from django.urls import path, include

from .board_views import (
    BoardListView,
    BoardCreate,
    BoardDetailView,
    BoardDeleteView,
    BoardUpdateView,
    archive_board,
    get_archived,
    preferred_boards,
    list_boards_preferred,
    last_seen,
)

from .column_views import (
    CreateColumnView,
    ColumnDetailView,
    ColumnUpdateView,
    delete_column
)

from .views import (
    about_page,
    home,
    SearchBoardResultView,
    SearchUserResultsView,
    get_user_board
)

    # Columns
from .card_views import (
    # Cards
    CreateCardView,
    CardDetailView,
    delete_card,
    UpdateCard
)

from .checklist_views import (
    # Checklist
    CreateChecklist,
    UpdateChecklist,
    delete_checklist,
)

from .mark_views import (
    # Mark
    CreateMark,
    UpdateMark,
    delete_mark,
    # Search functions
)

urlpatterns = [
    path("", home, name="home"),
    path("about/", about_page, name="about"),
    # Boards
    path("boards/", BoardListView.as_view(), name="boards"),
    path("boards_archived/", get_archived, name="boards_archived"),
    path("boards_last_seen/", last_seen, name="last_seen"),
    path("boards_preferred/", list_boards_preferred, name="list_boards_preferred"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board_view"),
    path("boards/<int:pk>/update/", BoardUpdateView.as_view(), name="board_update"),
    path("boards/<int:pk>/delete/", BoardDeleteView.as_view(), name="board_delete"),
    path("boards/add/", BoardCreate.as_view(), name="board-add"),
    path("boards/<int:pk>/archive/", archive_board, name="board_archive"),
    path("boards/<int:pk>/preferred/", preferred_boards, name="board_preferred"),
    # Columns
    path("boards/<int:pk>/columns/add/", CreateColumnView.as_view(), name="column-add"),
    path("boards/<int:pk>/columns/<int:column_id>/", ColumnDetailView.as_view(), name="column_view"),
    path("boards/<int:pk>/columns/<int:column_id>/delete/", delete_column, name="column_delete"),
    path("boards/<int:pk>/columns/<int:column_id>/update/", ColumnUpdateView.as_view(), name="column_update"),
    # Cards
    path("boards/<int:pk>/columns/<int:column_id>/cards/add/", CreateCardView.as_view(), name="card-add"),
    path("boards/<int:pk>/columns/<int:column_id>/cards/<int:card_id>/", CardDetailView.as_view(), name="card_view"),
    path("boards/<int:pk>/columns/<int:column_id>/cards/<int:card_id>/delete/", delete_card, name="card_delete"),
    path("boards/<int:pk>/columns/<int:column_id>/cards/<int:card_id>/update/", UpdateCard.as_view(), name="card_update"),
    # Checklist
    path("boards/<int:pk>/columns/<int:column_id>/cards/<int:card_id>/checklist/add", CreateChecklist.as_view(), name="checklist-add"),
    path("boards/<int:pk>/columns/<int:column_id>/cards/<int:card_id>/checklist/<int:checklist_id>/update",
         UpdateChecklist.as_view(), name="checklist-update"),
    path("boards/<int:pk>/columns/<int:column_id>/cards/<int:card_id>/checklist/<int:checklist_id>/delete",
         delete_checklist, name="checklist-delete"),
    # Mark
    path("boards/<int:pk>/columns/<int:column_id>/cards/<int:card_id>/mark/add", CreateMark.as_view(),
         name="mark-add"),
    path("boards/<int:pk>/columns/<int:column_id>/cards/<int:card_id>/mark/<int:mark_id>/update",
         UpdateMark.as_view(), name="mark-update"),
    path("boards/<int:pk>/columns/<int:column_id>/cards/<int:card_id>/mark/<int:mark_id>/delete",
         delete_mark, name="mark-delete"),
    # Search functions
    path("boards_search/", SearchBoardResultView.as_view(), name="search_board"),
    path("users_search/", SearchUserResultsView.as_view(), name="search_user"),
    path("users_search/<str:user_id>/", get_user_board, name="user_profile")
]
