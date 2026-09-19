package com.example.ermeydani





import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.input.TextObfuscationMode
import androidx.compose.foundation.text.input.rememberTextFieldState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.PlainTooltip
import androidx.compose.material3.SecureTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TooltipAnchorPosition
import androidx.compose.material3.TooltipBox
import androidx.compose.material3.TooltipDefaults
import androidx.compose.material3.rememberTooltipState
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.paneTitle
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.input.KeyboardType
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import retrofit2.HttpException
import androidx.compose.material3.ExperimentalMaterial3Api
class MainActivity : ComponentActivity() {

    @OptIn(ExperimentalMaterial3Api::class)
    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)

        setContent{
            var username by remember{mutableStateOf("")}
            var email by remember {mutableStateOf("")}
            var password by remember{mutableStateOf("")}
            val passwordState = rememberTextFieldState()
            var bio by remember{mutableStateOf("")}
            var showVerification by remember {mutableStateOf(false)}
            var verificationCode by remember {mutableStateOf("")}
            var isVerified by remember {mutableStateOf(false)}
            var accessToken by remember { mutableStateOf("") }
            var memories by remember {
                mutableStateOf(listOf<MemoryCreateResponse>())
            }
            var currentMemory by remember{mutableStateOf<MemoryCreateResponse?>(null)}
            var comments by remember {mutableStateOf(listOf<CommentDisplay>())}
            var commentCreationFields by remember{mutableStateOf(false)}
            var memoryTitle by remember {mutableStateOf("")}
            var memoryContent by remember {mutableStateOf("")}
            var currentUserMemories by remember {mutableStateOf(listOf<MemoryDisplay>())}
            var loginError by remember {mutableStateOf("")}
            var registerError by remember {mutableStateOf("")}
            var profileError by remember {mutableStateOf("")}
            var commentCreationError by remember {mutableStateOf("")}
            var emailVerificationError by remember {mutableStateOf("")}
            var memoryCreationError by remember{mutableStateOf("")}
            var currentScreen by remember {mutableStateOf("register")}


            var passwordHidden by rememberSaveable { mutableStateOf(true) }

            var commentCreationContent by remember{mutableStateOf("")}

            when(currentScreen){
                "register" -> {
                    Column{
                        OutlinedTextField(
                            value = username,
                            onValueChange = {username = it},
                            label = {Text("Username/E-mail")}
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
                                    try{
                                        RetrofitClient.api.register(request)
                                        showVerification = true
                                    }catch(e : HttpException){
                                        registerError = when(e.code()){
                                            409 -> "Username or Email is already Taken"
                                            else -> "Registration error : ${e.code()}"
                                        }
                                    }catch(e : Exception){
                                        registerError = "Can not connect to server please try again later!"
                                    }

                                }
                            }
                        ){
                            Text("Register Now!")
                        }
                        if (registerError.isNotEmpty()){
                            Text(registerError)
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
                                        try{
                                            val response = RetrofitClient.api.verifyEmail(verification)
                                            val status = response.status
                                            if (status.equals("success")){
                                                isVerified = true
                                                currentScreen = "login"
                                            }
                                            else{
                                                isVerified = false
                                            }
                                        }catch(e : HttpException){
                                            emailVerificationError = when(e.code()){
                                                400 -> "Verification code has expired!"
                                                404 -> "User not found, please register first."
                                                else -> "Verification Error: ${e.code()}"
                                            }

                                        }catch(e : Exception){
                                            emailVerificationError = "Connection with server lost!"
                                        }

                                    }
                                }
                            ){
                                Text("Verificate!")
                            }
                            if(emailVerificationError.isNotEmpty()){
                                Text(emailVerificationError)
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
                           label = {Text("Username/E-mail")}
                       )
                       SecureTextField(
                           state = passwordState,
                           label = {Text("Enter your password...")},
                           keyboardOptions =
                               KeyboardOptions(
                                   autoCorrectEnabled = false,
                                   keyboardType =
                                       if (passwordHidden) KeyboardType.Password else KeyboardType.PasswordVisible,
                               ),
                           textObfuscationMode = if (passwordHidden) TextObfuscationMode.System else TextObfuscationMode.Visible,
                           trailingIcon = {
                               val description =
                                   if (passwordHidden) "Show Password" else "Hide Password"
                               TooltipBox(
                                   positionProvider = TooltipDefaults.rememberTooltipPositionProvider(
                                       TooltipAnchorPosition.Above
                                   ),
                                   tooltip = {
                                       PlainTooltip(
                                           modifier = Modifier.semantics {
                                               liveRegion = LiveRegionMode.Assertive
                                               paneTitle = description
                                           }
                                       ) {
                                           Text(description)
                                       }
                                   },
                                   state = rememberTooltipState(),
                               ) {
                                   IconButton(onClick = { passwordHidden = !passwordHidden }) {
                                       val visibilityIcon =
                                           if (passwordHidden) Icons.Filled.Visibility else Icons.Filled.VisibilityOff
                                       Icon(
                                           imageVector = visibilityIcon,
                                           contentDescription = description
                                       )
                                   }
                               }
                           },
                       )
                       Button(
                           onClick = {
                               lifecycleScope.launch {
                                try{
                                    val passwordSend = passwordState.text.toString()
                                    val response = RetrofitClient.api.login(
                                        email = email,
                                        password = passwordSend
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
                            Button(
                                onClick = {
                                    comments = memory.comments
                                    currentMemory = memory
                                    currentScreen = "commentSection"
                                }
                            ){
                                Text("Comments")
                            }

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
                                    try{
                                        val response = RetrofitClient.api.createMemory(
                                            token = "Bearer $accessToken",
                                            createMemory = memory
                                        )
                                        memories = memories + response
                                        currentScreen = "home"
                                    }catch (e : HttpException){
                                        memoryCreationError = when(e.code()){
                                            422 -> "Memory should have title and content!"
                                            else -> "Memory Creation Error : ${e.code()}"
                                        }
                                    }catch(e : Exception){
                                        memoryCreationError = "Connection with server lost!"
                                    }
                                }
                            }
                        ){
                            Text("Share!")
                        }
                        if(memoryCreationError.isNotEmpty()){
                            Text(memoryCreationError)
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
                "commentSection" -> {
                    Column{
                        Text("Yorumlar")
                        Text("          ")
                        Text("          ")
                        Text("          ")
                        comments.forEach{ comment ->
                            Text(comment.user.username)
                            //Text(comment.user.profile_photo)
                            Text(comment.content)

                        }

                        Button(
                            onClick = {
                                commentCreationFields = true
                            }
                        ){
                            Text("Write Comment")
                        }


                        Button(
                            onClick = {
                                commentCreationFields = false
                                commentCreationContent = ""
                                commentCreationError = ""
                                currentScreen = "home"
                            }
                        ){
                            Text("Home")
                        }

                        if(commentCreationFields){
                            OutlinedTextField(
                                value = commentCreationContent,
                                onValueChange = {commentCreationContent = it},
                                label = {Text("Write...")}
                            )

                            Button(
                                onClick = {
                                    val newComment = CommentCreateRequest(
                                        content = commentCreationContent
                                    )
                                    currentMemory?.let {selectedMemory ->
                                        lifecycleScope.launch{
                                            try{
                                                val response = RetrofitClient.api.postComment(
                                                    memoryId = selectedMemory.id,
                                                    token = "Bearer $accessToken",
                                                    comment = newComment
                                                )

                                                val updatedComments = comments + response
                                                comments = updatedComments
                                                memories = memories.map{memory ->
                                                    if(memory.id == selectedMemory.id){
                                                        memory.copy(
                                                            comments = updatedComments
                                                        )
                                                    }else{
                                                        memory
                                                    }

                                                }
                                                currentMemory = selectedMemory.copy(
                                                    comments = updatedComments
                                                )
                                                commentCreationContent = ""
                                                commentCreationFields = false
                                                commentCreationError = ""
                                            }catch(e : HttpException){
                                                commentCreationError = when(e.code()){
                                                    400 -> "No content!"
                                                    404 -> "Memory not found!"
                                                    else -> "Comment Creation Error : ${e.code()}"

                                                }
                                            }catch(e : Exception){
                                                commentCreationError = "${e.javaClass.simpleName}: ${e.message}"
                                            }
                                        }
                                    }
                                }
                            ){
                                Text("Share")
                            }
                            if(commentCreationError.isNotEmpty()){
                                Text(commentCreationError)
                            }
                        }
                    }
                }
            }
        }
    }
}