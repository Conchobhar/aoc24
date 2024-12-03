import kotlin.math.abs

fun main() {

    fun part1(input: String): Int {
        val pattern = Regex("""mul\(([0-9]+),([0-9]+)\)""")
        val matches = pattern.findAll(input)
        var sum = 0
        for (match in matches) {
            val (g1, g2) = match.groupValues.drop(1).map { it.toInt() }
            sum += g1 * g2
        }
        return sum
    }

    fun part2(input: String): Int {
        val pattern = Regex("""mul\(([0-9]+),([0-9]+)\)|do\(\)|don't\(\)""")
        val matches = pattern.findAll(input)
        var sum = 0
        var switch = true
        for (match in matches) {
            val matchFull = match.groupValues[0]
            if ((matchFull[0] == 'm') and switch) {
                val (g1, g2) = match.groupValues.drop(1).map { it.toInt() }
                sum += g1 * g2
            } else {
                switch = when (matchFull) {
                    "do()" -> true
                    "don't()" -> false
                    else -> switch
                }
            }
        }
        return sum
    }
    val inputTest1 = "what()who(){from(),'mul(28,510)?<,>where()why()mul(276,283):#>mul(181,314)"
    val inputTest2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
//    check(part1(inputTest1) == 149222)
//    check(part2(inputTest2) == 48)

    val input = readInput("Day03")
    part1(input.joinToString(separator = "")).println()
    part2(input.joinToString(separator = "")).println()
}
