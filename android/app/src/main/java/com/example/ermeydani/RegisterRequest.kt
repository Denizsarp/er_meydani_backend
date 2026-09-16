package com.example.ermeydani

//User classes -----------------------------------------------------------------------------------
data class RegisterRequest(
    val username:String,
    val email:String,
    val password: String,
    val bio : String,
    val profile_photo : String
)

data class VerificationRequest(
    val email:String,
    val code:String
)


data class VerificationResponse(
    val message : String,
    val status : String
)

data class LoginResponse(
    val access_token : String,
    val token_type :String
)

data class UserDisplay(
    val username: String,
    val profile_photo: String?,
    val memories : List<MemoryCreateResponse>
)

//Memory classes -----------------------------------------------------------------------------------

data class MemoryCreateRequest(
    val title : String,
    val content : String
)

data class MemoryCreateResponse(
    val title:String,
    val content:String,
    val created_at : String,
    val user:UserDisplay,
    val comments:List<CommentDisplay>
)

data class MemoryDisplay(
    val title:String,
    val content:String,
    val created_at: String,
    val comments:List<CommentDisplay>
)



//Comment classes -----------------------------------------------------------------------------------

data class CommentDisplay(
    val content:String,
    val user : UserDisplay
)


