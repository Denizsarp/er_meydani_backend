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
                                RetrofitClient.api.verifyEmail(verification)
                            }
                        }
                    ){
                        Text("Verificate!")
                    }
                }
            }
        }


    }
}