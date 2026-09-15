package com.example.ermeydani


import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.GET
import retrofit2.http.DELETE

interface ApiService{
    @POST("auth/register")
    suspend fun register(
        @Body request:RegisterRequest
    )

    @POST("auth/verify-email")
    suspend fun verifyEmail(
        @Body verification : VerificationRequest
    )
}
