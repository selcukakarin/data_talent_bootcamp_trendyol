package com.example

import akka.actor.{Actor, ActorLogging, PoisonPill, Props}
import com.example.AkkaQuickstart.{Question, system}
import com.example.HumanActor.{Answer, Ask}

import scala.util.Random

class HumanActor(questions: List[Question]) extends Actor with ActorLogging {

  def customReceive(questions: List[Question]): Receive = {
    case Ask =>
      questions.headOption
        .map { question =>
          log.info(question.text)
          sender() ! Answer(question.possibleAnswers)
          context.become(customReceive(questions.tail))
        }
        .getOrElse {
          log.info("All question is asked")
          self ! PoisonPill
          system.terminate()
        }
    case Answer(possibleAnswers) =>
      val random = new Random()
      val index  = random.nextInt(possibleAnswers.length)

      log.info(possibleAnswers(index))
      Thread.sleep(1000)
      sender() ! Ask
  }

  override def receive: Receive = customReceive(questions)
}

object HumanActor {
  case object Ask
  case class Answer(possibleAnswers: List[String])
  def props(questions: List[Question]): Props = Props(new HumanActor(questions))
}
