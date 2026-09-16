package com.example.ermeydani

import android.os.Bundle
import android.os.PersistableBundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import retrofit2.HttpException
import kotlin.math.log


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent{
            var username by remember{mutableStateOf("")}
            var email by remember {mutableStateOf("")}
            var password by remember{mutableStateOf("")}
            var bio by remember{mutableStateOf("")}
            var showVerification by remember {mutableStateOf(false)}
            var verificationCode by remember {mutableStateOf("")}
            var isVerified by remember {mutableStateOf(false)}
            var accessToken by remember { mutableStateOf("") }
            var memories by remember {
                mutableStateOf(listOf<MemoryCreateResponse>())
            }
            var memoryTitle by remember {mutableStateOf("title")}
            var memoryContent by remember {mutableStateOf("")}
            var currentUserMemories by remember {mutableStateOf(listOf<MemoryDisplay>())}
            var loginError by remember {mutableStateOf("")}
            var profileError by remember {mutableStateOf("")}
            var currentScreen by remember {mutableStateOf("register")}

            when(currentScreen){
                "register" -> {
                    Column{
                        OutlinedTextField(
                            value = username,
                            onValueChange = {username = it},
                            label = {Text("Username")}
                        )

                        OutlinedTextField(
                            value = email,
                            onValueChange = {email = it},
                            label = {Text("email")}
                        )

                        OutlinedTextField(
                            value = password,
                            onValueChange = {password = it},
                            label = {Text("password")}
                        )
                        OutlinedTextField(
                            value = bio,
                            onValueChange = {bio = it},
                            label = {Text("bio")}
                        )

                        Button(
                            onClick = {
                                val request = RegisterRequest(
                                    username = username,
                                    email = email,
                                    password = password,
                                    bio = bio,
                                    profile_photo = ""
                                )
                                lifecycleScope.launch{
                                    RetrofitClient.api.register(request)
                                    showVerification = true
                                }
                            }
                        ){
                            Text("Register Now!")
                        }
                        Button(
                            onClick = {
                                currentScreen = "login"
                            }
                        ){
                            Text("Already registered? Login!")
                        }

                        if (showVerification){
                            OutlinedTextField(
                                value = verificationCode,
                                onValueChange = {verificationCode = it},
                                label = {Text("Verification Code")}
                            )

                            Button(
                                onClick = {
                                    val verification  = VerificationRequest(
                                        email = email,
                                        code = verificationCode
                                    )
                                    lifecycleScope.launch{
                                        val response = RetrofitClient.api.verifyEmail(verification)
                                        val status = response.status
                                        if (status.equals("success")){
                                            isVerified = true
                                            currentScreen = "login"
                                        }
                                        else{
                                            isVerified = false
                                        }
                                    }
                                }
                            ){
                                Text("Verificate!")
                            }
                        }
                    }

                }
               "login" -> {
                   Column{
                       Text("Login")

                       OutlinedTextField(
                           value = email,
                           onValueChange = {email = it},
                           label = {Text("Email")}
                       )
                       OutlinedTextField(
                           value = password,
                           onValueChange = {password = it},
                           label = {Text("Password")}
                       )
                       Button(
                           onClick = {
                               lifecycleScope.launch {
                                try{
                                    val response = RetrofitClient.api.login(
                                        email = email,
                                        password = password
                                    )
                                    accessToken = response.access_token
                                    memories = RetrofitClient.api.getAllMemories(
                                        token = "Bearer $accessToken"
                                    )
                                    currentScreen = "home"
                                }

                               catch (e: HttpException){
                                   loginError = when(e.code()){
                                       401 -> "Email or password is wrong"
                                       403 -> "Email is not verified yet!"
                                       else -> "Login error : ${e.code()}"
                                   }
                               }
                               catch(e : Exception){
                                   loginError = "can not connect server!"
                               }
                               }
                           }
                       ){
                           Text("Login")
                       }

                       if (loginError.isNotEmpty()){
                           Text(loginError)
                       }

                       Button(
                           onClick = {
                               currentScreen = "register"
                           }
                       ){
                           Text("Don't have account? Register now!")
                       }
                   }
               }
                "home" -> {
                    Column{
                        Text("Ana Sayfa")
                        Text("Memory Yarat")
                        memories.forEach{ memory ->
                            Text(memory.title)
                            Text(memory.content)

                            Text("Yazan: ${memory.user.username}")
                            Text("Oluşturulma: ${memory.created_at}")

                        }
                        Button(
                            onClick = {
                                currentScreen = "createMemory"
                            }
                        ){
                            Text("+")
                        }

                        Button(
                            onClick = {
                                lifecycleScope.launch{
                                    try{
                                        currentUserMemories = RetrofitClient.api.getMyMemories(
                                            token = "Bearer $accessToken"
                                        )
                                        currentScreen = "myProfile"

                                    }
                                    catch(e : Exception){
                                        profileError = "Can not load your profile!"
                                    }

                                }
                            }
                        ){
                            Text("My Profile")
                        }
                        if(profileError.isNotEmpty()){
                            Text(profileError)
                        }
                    }
                }
                "createMemory" -> {
                    Column{
                        Text("New Memory")

                        OutlinedTextField(
                            value = memoryTitle,
                            onValueChange = {memoryTitle = it},
                            label = {Text("Memory Title")}
                        )
                        OutlinedTextField(
                            value = memoryContent,
                            onValueChange = {memoryContent = it},
                            label = {Text("Write...")}
                        )

                        Button(
                            onClick = {
                                val memory = MemoryCreateRequest(
                                    title = memoryTitle,
                                    content = memoryContent
                                )
                                lifecycleScope.launch{

                                    val response = RetrofitClient.api.createMemory(
                                        token = "Bearer $accessToken",
                                        createMemory = memory
                                    )
                                    memories = memories + response
                                    currentScreen = "home"
                                }
                            }
                        ){
                            Text("Share!")
                        }
                    }
                }

                "myProfile" -> {
                    Column{
                        Text("My Profile")
                        currentUserMemories.forEach{ memory ->
                            Text(memory.title)
                            Text(memory.content)
                            Text("Oluşturulma: ${memory.created_at}")

                        }
                        Button(
                            onClick = {
                                currentScreen = "home"
                            }
                        ){
                            Text("Go main page")
                        }
                    }

                }

            }

        }


    }
}