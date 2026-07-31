import androidx.car.app.model.SearchTemplate
import androidx.car.app.model.Action

val b = SearchTemplate.Builder(object : SearchTemplate.SearchCallback {
    override fun onSearchSubmitted(searchText: String) {}
    override fun onSearchTextChanged(searchText: String) {}
}).setHeaderAction(Action.BACK).setShowKeyboardByDefault(false).build()
