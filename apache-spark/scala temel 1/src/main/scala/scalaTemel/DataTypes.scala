package scalaTemel

import math._
import scala.collection.immutable.Range
import scala.util.Random

object DataTypes {
  def main(args: Array[String]): Unit = {

    /*******  BYTE *********/
    // -128 ile 127 arasında tam sayı
    println("Byte, " + (-pow(2,7)) + " ile " + (pow(2,7) - 1) +" arasında tamsayı değer alır.")
    println("Byte " + Byte.MinValue + " ile " + Byte.MaxValue + " arasında değer alır.")

    val myByte:Byte = 127

    /*******  BOOLEAN  *********/
    // true veya false değerlerini alır
    println(1 == 2) // false yazdırır

    /*******  CHAR  *********/
    // unsigned max value 65535 kadar karakter alır
    // val c:Char = ': !' //gata verir
    val b:Char = '='
    //val c:Char = 'ee'

    /*******  SHORT  *********/
    // -32768 ile 32767 arasında tamsayı değer alır
    println("Short, " + Short.MinValue + " ile " + Short.MaxValue +" arasında tamsayı değer alır.")
    val myShort:Short = 32767
    //val myShort2:Short = 38000 // hata verir

    /*******  INT  *********/
    // -2147483648 ile 2147483647 arası değer alır
    println("Int, "+ Int.MinValue + " ile " + Int.MaxValue + " arasında tamsayı değer alır")

    /*******  LONG  *********/
    // -9223372036854775808 ile 9223372036854775807 arası değer alır
    println("Long, "+ Long.MinValue + " ile " + Long.MaxValue + " arasında tamsayı değer alır")

    /*******  FLOAT  *********/
    // -3.4028235E38 ile3.4028235E38 arası değer alır
    println("Float, " + Float.MinValue + " ile " + Float.MaxValue +" arasında tamsayı değer alır.")

    /*******  DOUBLE  *********/
    // -1.7976931348623157E308 ile 1.7976931348623157E308 arası değer alır
    println("Double, " + Double.MinValue + " ile " + Double.MaxValue +" arasında tamsayı değer alır.")

    /*******  BIGINT  *********/
    // Çok büyük rakamlar için
    println("BigInt: " + BigInt.apply("112312321343254365765765865243"))
    var myBigInt = BigInt("1232432534534234124354364567")
    println("myBigInt'e 1 ekledim: " + myBigInt +1)

    /*******  BIGDECIMAL  *********/
    // Çok büyük ondalıklı sayılar için
    println("BigDecimal: " + BigDecimal.apply("112312.211312353"))
    var myBigDecimal = BigDecimal("112312.21131235")
    println("myBigDecimal'e 1 ekledim: " + BigDecimal + 0.000000000000000001)

    /****************  Tür Dönüşümleri  ******************/

    /*
    Byte -> Short -> Int -> Long -> Float -> Double
    */

    val dbMax = Double.MaxValue

    println("DoubleMax: "+ dbMax + " Double to Int: " + dbMax.toInt)

    val intMax = Int.MaxValue
    println("IntMax: "+ intMax + " Int to Double: " + intMax.toDouble)

  }
}
