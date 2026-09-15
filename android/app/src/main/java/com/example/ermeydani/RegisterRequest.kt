package com.example.ermeydani

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