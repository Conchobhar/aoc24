import kotlin.math.abs

fun main() {

    fun isReportSafe(report: List<Int>): Int {
        // return 1 if safe else 0
        val delta0 = report[1] - report[0]
        val sign = when {
            delta0 > 0 -> 1
            delta0 < 0 -> -1
            else -> 0
        }
        report.windowed(2, 1).forEach { (v1, v2) ->
            val delta = v2 - v1
            if ((delta > 0) and (sign == -1)) {
                return 0
            } else if ((delta < 0) and (sign == 1)) {
                return 0
            }
            // if magnitude of delta is out of range
            if (abs(delta) !in 1..3) return 0
        }
        return 1
    }

    fun part1(input: List<String>): Int {
        // input is a list of strings where one string is like "67 69 71 72 75 78 76"
        var sum = 0
        input.forEach { item ->
            val report = item.split(' ').map{ it.toInt() }
            sum += isReportSafe(report)
        }
        return sum
    }

    fun part2(input: List<String>): Int {
        var sum = 0
        input.forEach { row ->
            val report = row.split(' ').map{ it.toInt() }
            if (isReportSafe(report) == 1) {
                sum += 1
            } else {
                for (i in report.indices) {
                    val dampenedReport = report.toMutableList().apply{ removeAt(i) }
                    if (isReportSafe(dampenedReport) == 1) {
                        sum += 1
                        break
                    }
                }
            }
        }
        return sum
    }
    val input = readInput("Day02")

    assert(isReportSafe(mutableListOf(1,2,7,8,9)) == 1)
    part1(input).println()
    part2(input).println()
}
