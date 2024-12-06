report 50600 "FS Day 06"
{
    UsageCategory = ReportsAndAnalysis;
    ApplicationArea = All;
    ProcessingOnly = true;
    UseRequestPage = false;

    trigger OnPreReport()
    begin
        Codeunit.Run(Codeunit::"FS Day 06");
    end;
}

codeunit 50600 "FS Day 06"
{
    trigger OnRun()
    begin
        ParseInput();

        if (StartingRow = 0) or (StartingCol = 0) then
            Error('Starting position not found');

        Solve();
    end;

    var
        MapEntry: Record "FS Map Entry";
        StartingDirection: Option Up,Right,Down,Left;
        StartingRow, StartingCol : Integer;
        Rows, Cols : Integer;

    local procedure ParseInput()
    var
        FileManagement: Codeunit "File Management";
        TempBlob: Codeunit "Temp Blob";
        InStream: InStream;
        Line: Text;
        Char: Char;
        Row, Col : Integer;
    begin
        if FileManagement.BLOBImport(TempBlob, 'input') = '' then
            Error('');

        InStream := TempBlob.CreateInStream();

        Row := 1;
        while not InStream.EOS do begin
            InStream.ReadText(Line);

            Col := 1;
            foreach Char in Line do begin
                if Char = '#' then
                    MapEntry.Create(Row, Col)
                else if Char <> '.' then begin
                    case Char of
                        'v':
                            StartingDirection := StartingDirection::Down;
                        '>':
                            StartingDirection := StartingDirection::Right;
                        '<':
                            StartingDirection := StartingDirection::Left;
                        '^':
                            StartingDirection := StartingDirection::Up;
                        else
                            Error('Unexpected char %1', Char);
                    end;

                    StartingRow := Row;
                    StartingCol := Col;
                end;

                Col += 1;
            end;

            Row += 1;
        end;

        Rows := Row - 1;
        Cols := Col - 1;
    end;

    local procedure Solve()
    var
        VisitedRows: Record "FS Range";
        VisitedCols: Record "FS Range";
        Row, Col, i : Integer;
        NextRow, NextCol : Integer;
        Direction: Option;
        Result: Record "FS Map Entry";
        Found: Boolean;
    begin
        Row := StartingRow;
        Col := StartingCol;
        Direction := StartingDirection;

        Found := true;
        while Found do begin
            MapEntry.Reset();

            case Direction of
                StartingDirection::Up:
                    begin
                        MapEntry.SetFilter(Row, '<%1', Row);
                        MapEntry.SetRange(Column, Col);
                        Found := MapEntry.FindLast();
                        if not Found then
                            MapEntry.Row := 0;

                        NextRow := MapEntry.Row + 1;

                        for i := Row downto NextRow + 1 do
                            TestLoop(Result, VisitedRows, VisitedCols, i, Col, Direction, i - 1, Col);

                        VisitedCols.Create(Col, Row, NextRow);
                        Row := NextRow;
                    end;
                StartingDirection::Right:
                    begin
                        MapEntry.SetFilter(Column, '>%1', Col);
                        MapEntry.SetRange(Row, Row);
                        Found := MapEntry.FindFirst();
                        if not Found then
                            MapEntry.Column := Cols + 1;

                        NextCol := MapEntry.Column - 1;

                        for i := Col to NextCol - 1 do
                            TestLoop(Result, VisitedRows, VisitedCols, Row, i, Direction, Row, i + 1);

                        VisitedRows.Create(Row, Col, NextCol);
                        Col := NextCol;
                    end;
                StartingDirection::Down:
                    begin
                        MapEntry.SetFilter(Row, '>%1', Row);
                        MapEntry.SetRange(Column, Col);
                        Found := MapEntry.FindFirst();
                        if not Found then
                            MapEntry.Row := Rows + 1;

                        NextRow := MapEntry.Row - 1;

                        for i := Row to NextRow - 1 do
                            TestLoop(Result, VisitedRows, VisitedCols, i, Col, Direction, i + 1, Col);

                        VisitedCols.Create(Col, Row, NextRow);
                        Row := NextRow;
                    end;
                StartingDirection::Left:
                    begin
                        MapEntry.SetFilter(Column, '<%1', Col);
                        MapEntry.SetRange(Row, Row);
                        Found := MapEntry.FindLast();
                        if not Found then
                            MapEntry.Column := 0;

                        NextCol := MapEntry.Column + 1;

                        for i := Col downto NextCol + 1 do
                            TestLoop(Result, VisitedRows, VisitedCols, Row, i, Direction, Row, i - 1);

                        VisitedRows.Create(Row, Col, NextCol);
                        Col := NextCol;
                    end;
            end;

            Direction := (Direction + 1) mod 4;
        end;

        Message('Visited %1', CountVisited(VisitedRows, VisitedCols));
        Message('Obstructions %1', Result.Count());
    end;

    local procedure CountVisited
    (
        var VisitedRows: Record "FS Range";
        var VisitedCols: Record "FS Range"
    ): Integer
    var
        i: Integer;
    begin
        VisitedRows.Reset();
        if VisitedRows.FindSet() then
            repeat
                i += VisitedRows."To" - VisitedRows.From + 1;
            until VisitedRows.Next() = 0;

        VisitedCols.Reset();
        if VisitedCols.FindSet() then
            repeat
                i += VisitedCols."To" - VisitedCols.From + 1;

                VisitedRows.SetRange(At, VisitedCols.From, VisitedCols."To");
                VisitedRows.SetFilter(From, '..%1', VisitedCols.At);
                VisitedRows.SetFilter("To", '%1..', VisitedCols.At);
                i -= VisitedRows.Count();
            until VisitedCols.Next() = 0;

        exit(i);
    end;



    local procedure Visited
    (
        var VisitedRows: Record "FS Range";
        var VisitedCols: Record "FS Range";
        Row: Integer;
        Col: Integer
    ): Boolean
    begin
        VisitedRows.Reset();
        VisitedRows.SetRange(At, Row);
        VisitedRows.SetFilter(From, '..%1', Col);
        VisitedRows.SetFilter("To", '%1..', Col);
        if not VisitedRows.IsEmpty() then
            exit(true);

        VisitedCols.Reset();
        VisitedCols.SetRange(At, Col);
        VisitedCols.SetFilter(From, '..%1', Row);
        VisitedCols.SetFilter("To", '%1..', Row);
        if not VisitedCols.IsEmpty() then
            exit(true);

        exit(false);
    end;

    local procedure TestLoop
    (
        var Result: Record "FS Map Entry";
        var VisitedRows: Record "FS Range";
        var VisitedCols: Record "FS Range";
        Row: Integer;
        Col: Integer;
        Direction: Option;
        ObstacleRow: Integer;
        ObstacleCol: Integer
    )
    var
        MapEntryCopy: Record "FS Map Entry";
    begin
        if (ObstacleRow = StartingRow) and (ObstacleCol = StartingCol) then
            exit;
        if Result.Get(ObstacleRow, ObstacleCol) then
            exit;
        if Visited(VisitedRows, VisitedCols, ObstacleRow, ObstacleCol) then
            exit;

        MapEntryCopy.Copy(MapEntry, true);
        MapEntryCopy.Create(ObstacleRow, ObstacleCol);

        if Loops(Row, Col, Direction) then
            Result.Create(ObstacleRow, ObstacleCol);

        MapEntryCopy.Delete();
    end;

    local procedure Loops(LoopRow: Integer; LoopCol: Integer; LoopDirection: Option): Boolean
    var
        Row, Col : Integer;
        Direction: Option;
        Visited: Record "FS Map Entry with Direction";
    begin
        Row := LoopRow;
        Col := LoopCol;
        Direction := LoopDirection;

        while true do begin
            MapEntry.Reset();

            case Direction of
                StartingDirection::Up:
                    begin
                        MapEntry.SetFilter(Row, '<%1', Row);
                        MapEntry.SetRange(Column, Col);
                        if not MapEntry.FindLast() then
                            exit(false);

                        Row := MapEntry.Row + 1;
                    end;
                StartingDirection::Right:
                    begin
                        MapEntry.SetFilter(Column, '>%1', Col);
                        MapEntry.SetRange(Row, Row);
                        if not MapEntry.FindFirst() then
                            exit(false);

                        Col := MapEntry.Column - 1;
                    end;
                StartingDirection::Down:
                    begin
                        MapEntry.SetFilter(Row, '>%1', Row);
                        MapEntry.SetRange(Column, Col);
                        if not MapEntry.FindFirst() then
                            exit(false);

                        Row := MapEntry.Row - 1;
                    end;
                StartingDirection::Left:
                    begin
                        MapEntry.SetFilter(Column, '<%1', Col);
                        MapEntry.SetRange(Row, Row);
                        if not MapEntry.FindLast() then
                            exit(false);

                        Col := MapEntry.Column + 1;
                    end;
            end;

            if Visited.Get(Row, Col, Direction) then
                exit(true);
            Visited.Create(Row, Col, Direction);

            Direction := (Direction + 1) mod 4;
        end;
    end;
}

table 50600 "FS Map Entry"
{
    TableType = Temporary;

    fields
    {
        field(1; Row; Integer) { }
        field(2; Column; Integer) { }
    }

    keys
    {
        key(PK; Row, Column)
        {
            Clustered = true;
        }
    }

    procedure Create(NewRow: Integer; NewCol: Integer)
    begin
        Rec.Init();
        Rec.Row := NewRow;
        Rec.Column := NewCol;
        Rec.Insert();
    end;
}

table 50601 "FS Range"
{
    TableType = Temporary;

    fields
    {
        field(1; At; Integer) { }
        field(2; From; Integer) { }
        field(3; "To"; Integer) { }
    }

    keys
    {
        key(PK; At, From, "To")
        {
            Clustered = true;
        }
    }

    procedure Create(NewAt: Integer; NewFrom: Integer; NewTo: Integer)
    begin
        if Merge(NewAt, NewFrom, NewTo) then
            exit;

        Rec.Init();
        Rec.At := NewAt;
        Rec.From := Min(NewFrom, NewTo);
        Rec."To" := Max(NewFrom, NewTo);
        Rec.Insert();
    end;

    local procedure Merge(NewAt: Integer; NewFrom: Integer; NewTo: Integer): Boolean
    var
        Merged: Boolean;
    begin
        Rec.SetRange(At, NewAt);

        // if contained, exit
        Rec.SetFilter(From, '..%1', NewFrom);
        Rec.SetFilter("To", '%1..', NewTo);
        if not Rec.IsEmpty() then
            exit(true);

        // delete contained ranges
        Rec.SetFilter(From, '%1..', NewFrom);
        Rec.SetFilter("To", '..%1', NewTo);
        Rec.DeleteAll();

        Rec.SetRange(From);
        Rec.SetRange("To", NewFrom, NewTo);
        if Rec.FindFirst() then begin
            Rec.Rename(Rec.At, Rec.From, NewTo);
            Merged := true;
        end;

        Rec.SetRange(From, NewFrom, NewTo);
        Rec.SetRange("To");
        if Rec.FindFirst() then begin
            Rec.Rename(Rec.At, NewFrom, Rec."To");
            Merged := true;
        end;

        exit(Merged);
    end;

    local procedure Min(a: Integer; b: Integer): Integer
    begin
        if a < b then
            exit(a);
        exit(b);
    end;

    local procedure Max(a: Integer; b: Integer): Integer
    begin
        if a > b then
            exit(a);
        exit(b);
    end;
}

table 50602 "FS Map Entry with Direction"
{
    TableType = Temporary;

    fields
    {
        field(1; Row; Integer) { }
        field(2; Column; Integer) { }
        field(3; Direction; Integer) { }
    }

    keys
    {
        key(PK; Row, Column, Direction)
        {
            Clustered = true;
        }
    }

    procedure Create(NewRow: Integer; NewCol: Integer; NewDirection: Integer)
    begin
        Rec.Init();
        Rec.Row := NewRow;
        Rec.Column := NewCol;
        Rec.Direction := NewDirection;
        Rec.Insert();
    end;
}