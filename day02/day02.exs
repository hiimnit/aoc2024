defmodule Exercise do
  def is_safe(report) do
    is_in_range(report) && (is_ascending(report) || is_descending(report))
  end

  def is_safe_with_tolerance(report) do
    report_with_index = Enum.with_index(report)

    permutations =
      Enum.map(0..(length(report) - 1), fn i ->
        Enum.filter(report_with_index, fn {_, v} -> v != i end)
        |> Enum.map(fn {k, _} -> k end)
      end)

    is_safe(report) || Enum.any?(permutations, fn e -> Exercise.is_safe(e) end)
  end

  def is_in_range(report) do
    Enum.zip(report, Enum.slice(report, 1, length(report) - 1))
    |> Enum.all?(fn {a, b} -> abs(a - b) >= 1 && abs(a - b) <= 3 end)
  end

  def is_ascending(report) do
    Enum.zip(report, Enum.slice(report, 1, length(report) - 1))
    |> Enum.all?(fn {a, b} -> a < b end)
  end

  def is_descending(report) do
    Enum.zip(report, Enum.slice(report, 1, length(report) - 1))
    |> Enum.all?(fn {a, b} -> a > b end)
  end
end

[file_name] = System.argv()

input =
  File.stream!(file_name)
  |> Stream.map(fn e ->
    String.trim(e) |> String.split(" ") |> Enum.map(fn e -> String.to_integer(e) end)
  end)
  |> Enum.to_list()

result =
  Enum.filter(input, fn line -> Exercise.is_safe(line) end)
  |> Enum.count()

IO.puts("p1: " <> Integer.to_string(result))

result =
  Enum.filter(input, fn line -> Exercise.is_safe_with_tolerance(line) end)
  |> Enum.count()

IO.puts("p2: " <> Integer.to_string(result))
