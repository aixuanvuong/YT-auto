package com.example.car

import androidx.car.app.CarContext
import androidx.car.app.Screen
import androidx.car.app.model.Action
import androidx.car.app.model.ActionStrip
import androidx.car.app.model.CarIcon
import androidx.car.app.model.GridItem
import androidx.car.app.model.GridTemplate
import androidx.car.app.model.ItemList
import androidx.car.app.model.Template
import androidx.core.graphics.drawable.IconCompat
import com.example.R

class MainScreen(carContext: CarContext) : Screen(carContext) {
    override fun onGetTemplate(): Template {
        val searchIcon = CarIcon.Builder(IconCompat.createWithResource(carContext, R.drawable.ic_search_car)).build()
        val trendingIcon = CarIcon.Builder(IconCompat.createWithResource(carContext, R.drawable.ic_trending_car)).build()
        
        val list = ItemList.Builder()
            .addItem(
                GridItem.Builder()
                    .setTitle("Tìm kiếm")
                    .setText("Tìm video YouTube")
                    .setImage(searchIcon)
                    .setOnClickListener {
                        screenManager.push(SearchScreen(carContext))
                    }
                    .build()
            )
            .addItem(
                GridItem.Builder()
                    .setTitle("Thịnh hành")
                    .setText("Video nổi bật")
                    .setImage(trendingIcon)
                    .setOnClickListener {
                        // For demonstration
                    }
                    .build()
            )
            .build()
            
        val searchAction = Action.Builder()
            .setIcon(searchIcon)
            .setOnClickListener {
                screenManager.push(SearchScreen(carContext))
            }
            .build()
            
        val actionStrip = ActionStrip.Builder()
            .addAction(searchAction)
            .build()
            
        return GridTemplate.Builder()
            .setTitle("YouTube Auto")
            .setHeaderAction(Action.APP_ICON)
            .setActionStrip(actionStrip)
            .setSingleList(list)
            .build()
    }
}
