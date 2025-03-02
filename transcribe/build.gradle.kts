plugins {
    application
}

group = "jorjao81.zh"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}

application {
    mainClass = "jorjao81.zh.Main"
}


tasks.test {
    useJUnitPlatform()
}