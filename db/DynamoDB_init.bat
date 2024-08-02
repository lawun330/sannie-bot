
REM This batch file is used to start the DynamoDBLocal database with the specified library path and jar file.
REM You can use the following command to start the database, assuming the current directory is the parent of the DynamoDBLocal_lib directory:
REM "C:\Program Files\Java\jdk-17\bin\java.exe" -Djava.library.path=./DynamoDBLocal_lib -jar
REM DynamoDBLocal.jar -sharedDb


@echo off
REM Set the path to the Java executable
set JAVA_PATH="C:\Program Files\Java\jdk-17\bin\java.exe"

REM Set the path to the parent directory of the DynamoDBLocal library
set DYNAMODB_LIB_PARENT_PATH="C:\dynamodb_local_latest"

REM Set the path to the DynamoDBLocal library
set DYNAMODB_LIB_PATH=".\DynamoDBLocal_lib"

REM Set the path to the DynamoDBLocal JAR file
set DYNAMODB_JAR_PATH=DynamoDBLocal.jar

REM Change the current directory to the parent path
cd %DYNAMODB_LIB_PARENT_PATH%

REM Run the DynamoDBLocal JAR file with the specified library path
%JAVA_PATH% -Djava.library.path=%DYNAMODB_LIB_PATH% -jar %DYNAMODB_JAR_PATH% -sharedDb

pause