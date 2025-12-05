import kotlin.math.abs

fun main() {
    fun part1(input: List<String>): Int {
        val l1: MutableList<Int> = mutableListOf()
        val l2: MutableList<Int> = mutableListOf()
        val diff: MutableList<Int> = mutableListOf()
        input.forEach { item ->
            val (i1, i2) = item.split("   ").map{ it.toInt() }
            l1.add(i1)
            l2.add(i2)
        }
        l1.sort(); l2.sort()
        l1.zip(l2).forEach { (i1, i2) ->
            diff.add(abs(i2 - i1))
        }
        return diff.sum()
    }

    fun part2(input: List<String>): Int {
        val l1: MutableList<Int> = mutableListOf()
        val m2: MutableMap<Int, Int> = mutableMapOf()
        input.forEach { item ->
            val (i1, i2) = item.split("   ").map{ it.toInt() }
            l1.add(i1)
            m2[i2] = m2[i2]?.plus(1) ?: 1
        }
        var sum = 0
        l1.forEach { i1 ->
            // rolling sum of (k*v if k in m2 else 0)
            sum  += m2[i1]?.times(i1) ?: 0
        }
        return sum
    }
    val input = readInput("Day01")
    part1(input).println()
    part2(input).println()
}
