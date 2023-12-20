package scalaTemel

object Maps {
  def main(args: Array[String]): Unit = {

    /****************  IMMUTEABLE MAP   *************************/
    // Immutable Map oluşturma
    val ulkeBaskent = Map("Japonya"->"Tokyo",  //immutable
      "Hindistan" -> "Delhi",
      "Güney Kore" -> "Seul")
    println("ulkeBaskent: " + ulkeBaskent)

    // Başka bir yöntemle oluşturalım
    val ulkeBaskent2 = Map(("ABD","Washington"), ("Fransa","Paris"))
    println("ulkeBaskent2: " + ulkeBaskent2)

    // if ile eğer bir ülke Map içinde var ise başkentini yazdırsın
    var anahtar = "Almanya"
    if(ulkeBaskent.contains(anahtar)){
      println(s"Aranılan ülke $anahtar  başkenti : " + ulkeBaskent(anahtar))
    }else{
      println(s"Aranılan ${anahtar}, ülkeler içinde yok.")
    }

    // Immutable bir Map'e eleman eklenemez
    // ulkeBaskent("Almanya") = "Berlin" // immutable.Map olduğu için hata verir


    /****************  MUTEABLE MAP   *************************/

    // Mutable Map oluşturmak
    val ulkeBaskentMut = collection.mutable.Map("Japonya"->"Tokyo",  //muteable
      "Hindistan" -> "Delhi",
      "Güney Kore" -> "Seul")

    // Mutable Map'e eleman ekleme
    ulkeBaskentMut("Almanya") = "Berlin" // mutable.Map olduğu için kabul eder

    // Muteable Map'a başka bir yöntemle eleman ekleme
    ulkeBaskentMut += ("İspanya" -> "Madrid")

    println(ulkeBaskentMut)

    // if ile eğer bir ülke Map içinde var ise başkentini yazdırsın.
    // Almanya'yı ekleyebildiğimize göre
    if(ulkeBaskentMut.contains(anahtar)){
      println(s"Aranılan ülke $anahtar  başkenti :" + ulkeBaskentMut(anahtar))
    }else{
      println(s"Aranılan ${anahtar}, ülkeler içinde yok.")
    }

    val ogrenciler = collection.mutable.Map(1503 -> "Salih",
      1504 -> "Hasan",
      1505 -> "Tuncay")

    ogrenciler(1508) = "Mustafa"

    println(ogrenciler)

    // Map içinden anahtar ile değer çağırmak
    println(ogrenciler(1503))

    // Map içinden anahtar ile değer çağırmak
    //println(ogrenciler(1000))  // hata verir


    // Map ile get kullanarak olmayan bir anahtar ile değer çağırmak
    println(ogrenciler.get(1505)) // Hata vermez None döndürür
    println(ogrenciler.get(1))

    // Sadece Map anahtarlarına ulaşmak
    println("ulkeBaskentMut.keys: " + ulkeBaskentMut.keys)
    println("ulkeBaskent.keys: " + ulkeBaskent.keys)


    // Sadece Map değerlerine ulaşmak
    println("ulkeBaskentMut.values: " + ulkeBaskentMut.values)
    println("ulkeBaskent.values: " + ulkeBaskent.values)
  }
}
