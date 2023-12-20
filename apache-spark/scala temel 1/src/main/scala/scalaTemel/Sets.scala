package scalaTemel

object Sets {
  def main(args: Array[String]): Unit = {
    // Boş immutable bir Set oluşturmak
    val myImmutSet = Set()

    // Tekrarlayanları atlar
    val myImmutSet2 = Set(1,1,1,2,2,3,5,5,4,4)
    println("Tekrardan kurtulan myImmutSet2: " + myImmutSet2)

    // Veri türü karışık olan Set
    val myImmutSet3 = Set("Merhaba", 3.5, 3, "Ankara","Ankara","Niğde",true)
    println("Karışık veri türündeki myImmutSet3 : " + myImmutSet3)


    // Veri türünde string bulunan setleri toplayamayız
    //myImmutSet3.sum

    // Setlerde indeks yoktur ve sırasızdır
    // Diğer collectionlarda elemana erişim için kullanılan myCollection(index)
    // Setlerde elemana erişim için değil elemanın varlığının kontrolü için çalışır.
    println("myImmutSet2 içinde 100 var mı? : " + myImmutSet2(100))
    println("myImmutSet3 içinde Ankara var mı? : " + myImmutSet3("Ankara"))

    // Set elemanlarını sıralayamayız
    //myImmutSet2.sort //hata verir


    /************** MUTEABLE SET OLUŞTURMAK  *********************/
    // Muteable Set oluşturmak
    val myMuteSet = scala.collection.mutable.Set(3,8,11,27)

    // Muteable Set'e eleman eklemek
    myMuteSet += 5
    println("myMuteSet'e + ile eleman ekleme : " + myMuteSet)

    // Immutable Set'e add metoduyle eleman eklemek
    myMuteSet.add(99)
    println("myMuteSet'e add() metoduyla eleman ekleme : " + myMuteSet)

    println("myMuteSet toplamı: " + myMuteSet.sum)

    // Listeyi Set'e dönüştürmek
    val myList = List(9,2,5,4,2,9)
    val setFromList = myList.toSet
    println("setFromList: " + setFromList)

    /*************** SET OPERASYONLARI  ************/
    println("myImmutSet2: " + myImmutSet2)

    // Kesişim
    println("Intersect" + setFromList.intersect(myImmutSet2))

    // İki küme farkı
    println("setFromList - myImmutSet2: " + setFromList.diff(myImmutSet2))

    // tersini yapalım
    println("myImmutSet2 - setFromList: " + myImmutSet2.diff(setFromList))

    // İki küme birleşimi
    println("İki küme birleşimi: " +myImmutSet2.union(setFromList))

  }
}
