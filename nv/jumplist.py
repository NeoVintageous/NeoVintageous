from Default.history_list import get_jump_history


def jumplist_update(view):
    # type: (...) -> None
    get_jump_history(view.window().id()).push_selection(view)
