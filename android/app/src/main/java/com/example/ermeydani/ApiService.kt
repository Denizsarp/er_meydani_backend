package com.example.ermeydani


import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.GET
import retrofit2.http.DELETE
import retrofit2.http.FormUrlEncoded
import retrofit2.http.Field
import retrofit2.http.Header

interface ApiService{
    //User Methods -----------------------------------------------------------------------------------
    @POST("auth/register")
    suspend fun register(
        @Body request:RegisterRequest
    )

    @POST("auth/verify-email")
    suspend fun verifyEmail(
        @Body verification : VerificationRequest
    ): VerificationResponse


    @FormUrlEncoded
    @POST("/auth/login")
    suspend fun login(
        @Field("username") email : String,
        @Field("password") password : String
    ):LoginResponse


    //Memory Methods -----------------------------------------------------------------------------------

    @POST("/memories/create")
    suspend fun createMemory(
        @Header("Authorization") token : String,
        @Body createMemory : MemoryCreateRequest
    ): MemoryCreateResponse

}
