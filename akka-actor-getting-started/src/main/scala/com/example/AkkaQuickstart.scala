package com.example

import akka.actor.{ActorRef, ActorSystem, PoisonPill}
import akka.pattern.ask
import com.example.HumanActor.Ask

object AkkaQuickstart extends App {
  case class Question(text: String, possibleAnswers: List[String])

  val questions: List[Question] = List(
    Question("Merhaba", possibleAnswers = List("selam", "slm", "as", "asl")),
    Question("Naber", possibleAnswers = List("iyidir", "kötüyüm", "hic sorma ya", "ne sen sor ne ben soyleyeyim")),
    Question(
      "Napıyorsun",
      possibleAnswers = List("Ders dinliyorum", "oturuyorum kendime", "Akka ile live coding yapiyorum")
    )
  )

  val system: ActorSystem = ActorSystem()

  val humanActor: ActorRef = system.actorOf(HumanActor.props(questions), "humanActor")

//  humanActor.ask(Ask)
  humanActor.tell(Ask, humanActor)

//  humanActor ! PoisonPill
//
//  system.terminate()

}
