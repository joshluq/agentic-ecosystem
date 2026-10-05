package com.example.feature.ui

import androidx.compose.runtime.Immutable
import androidx.lifecycle.SavedStateHandle
import dagger.hilt.android.lifecycle.HiltViewModel
import es.joshluq.foundationkit.viewmodel.ScreenViewModel
import es.joshluq.foundationkit.viewmodel.UiAction
import es.joshluq.foundationkit.viewmodel.UiEffect
import es.joshluq.foundationkit.viewmodel.UiState
import javax.inject.Inject

// 1. Immutable State
@Immutable
data class FeatureUiState(
    val isLoading: Boolean = false,
    val title: String = "",
    val errorMessage: String? = null
) : UiState

// 2. Sealed Action Hierarchy (User Events)
sealed interface FeatureUiAction : UiAction {
    data object Refresh : FeatureUiAction
    data class Submit(val query: String) : FeatureUiAction
}

// 3. Sealed One-Off Effects (Navigation, Toast)
sealed interface FeatureUiEffect : UiEffect {
    data class NavigateToDetails(val id: String) : FeatureUiEffect
    data class ShowToast(val message: String) : FeatureUiEffect
}

// 4. ViewModel implementation
@HiltViewModel
class FeatureViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle
) : ScreenViewModel<FeatureUiState, FeatureUiAction, FeatureUiEffect>() {

    override fun createInitialState(): FeatureUiState = FeatureUiState()

    override fun handleEvent(event: FeatureUiAction) {
        when (event) {
            is FeatureUiAction.Refresh -> updateState { copy(isLoading = true) }
            is FeatureUiAction.Submit -> launchEffect(FeatureUiEffect.NavigateToDetails(event.query))
        }
    }
}
