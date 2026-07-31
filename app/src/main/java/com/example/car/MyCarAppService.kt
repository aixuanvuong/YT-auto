package com.example.car

import android.content.Intent
import androidx.car.app.CarAppService
import androidx.car.app.Screen
import androidx.car.app.Session
import androidx.car.app.validation.HostValidator

class MyCarAppService : CarAppService() {
    override fun createHostValidator(): HostValidator {
        return HostValidator.ALLOW_ALL_HOSTS_VALIDATOR
    }

    override fun onCreateSession(): Session {
        return MySession()
    }
}

class MySession : Session() {
    override fun onCreateScreen(intent: Intent): Screen {
        return handleIntent(intent) ?: MainScreen(carContext)
    }

    override fun onNewIntent(intent: Intent) {
        val screen = handleIntent(intent)
        if (screen != null) {
            carContext.getCarService(androidx.car.app.ScreenManager::class.java).push(screen)
        }
    }

    private fun handleIntent(intent: Intent): Screen? {
        if (intent.action == Intent.ACTION_SEARCH || intent.action == "com.google.android.gms.actions.SEARCH_ACTION") {
            val query = intent.getStringExtra(Intent.EXTRA_TEXT) ?: intent.getStringExtra("query")
            if (query != null) {
                return SearchScreen(carContext, query)
            }
        }
        return null
    }
}
