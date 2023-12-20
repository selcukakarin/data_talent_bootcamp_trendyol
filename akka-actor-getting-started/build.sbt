name := "akka-quickstart-scala"

version := "1.0"

scalaVersion := "2.13.1"

lazy val akkaVersion = "2.5.23"

libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-actor"     % akkaVersion,
  "ch.qos.logback"    % "logback-classic" % "1.2.3",
  "org.scalatest"     %% "scalatest"      % "3.1.0" % Test
)
