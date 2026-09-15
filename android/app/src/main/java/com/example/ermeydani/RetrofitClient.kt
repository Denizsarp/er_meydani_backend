package com.example.ermeydani

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient{
    private const val FASTAPI_URL = "http://10.0.2.2:8000/"

    val api : ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(FASTAPI_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}

