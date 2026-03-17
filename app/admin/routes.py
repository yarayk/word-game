from aiohttp.web_app import Application

__all__ = ("register_urls",)


def register_urls(application: Application) -> None:
    from app.admin.views import (
        BroadcastView,
        GameDetailView,
        GameListView,
        GamesStopAllView,
        GameStopView,
        StatsView,
        admin_index,
        admin_page,
        stop_games_page,
    )

    application.router.add_get("/admin", admin_index)
    application.router.add_get("/stats", admin_page)
    application.router.add_view("/api/admin/games", GameListView)
    application.router.add_view("/api/admin/games/stop_all", GamesStopAllView)
    application.router.add_view("/api/admin/games/{id}", GameDetailView)
    application.router.add_view("/api/admin/games/{id}/stop", GameStopView)
    application.router.add_view("/api/admin/stats", StatsView)
    application.router.add_view("/api/admin/broadcast", BroadcastView)
    application.router.add_get("/stop-games", stop_games_page)
