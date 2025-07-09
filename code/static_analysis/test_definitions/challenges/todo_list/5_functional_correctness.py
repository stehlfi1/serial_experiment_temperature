"""
Test for correct implementation of the functions (internal)
Running: pytest 3_functional_correctness.py
Output: pytest report
"""

import pytest


# from chatgpt import TaskManager
# from claude import TaskManager
# from gemini import TaskManager


@pytest.fixture
def manager():
    return TaskManager()


@pytest.fixture(autouse=True)
def clear_tasks(manager):
    manager.clear_all()


# ---------------------------------------------------------------------
def test_init_task_list_empty(manager):
    assert manager.get_all() == []


# ---------------------------------------------------------------------
def test_add(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")
    manager.add("task_name4", "task_description4")
    assert len(manager.get_all()) == 4


def test_add_long_task_name(manager):
    manager.add("task_name1" * 1000, "task_description1")
    assert len(manager.get_all()) == 1


def test_add_long_task_description(manager):
    manager.add("task_name1", "task_description1" * 1000)
    assert len(manager.get_all()) == 1


def test_add_too_many_tasks(manager):
    for i in range(10000):
        manager.add(f"task_name{i}", f"task_description{i}")
    assert len(manager.get_all()) == 10000


def test_add_multiple_same_tasks(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name1", "task_description1")
    manager.add("task_name1", "task_description1")
    manager.add("task_name1", "task_description1")
    assert len(manager.get_all()) == 4


def test_add_return_type(manager):
    assert isinstance(manager.add("task_name1", "task_description1"), int)
    assert isinstance(manager.add("task_name2", "task_description2"), int)
    assert isinstance(manager.add("task_name3", "task_description3"), int)
    assert isinstance(manager.add("task_name4", "task_description4"), int)


def test_add_with_empty_name(manager):
    with pytest.raises(ValueError):
        manager.add("", "task_description")


def test_add_with_empty_description(manager):
    with pytest.raises(ValueError):
        manager.add("task_name", "")


def test_add_with_empty_name_and_description(manager):
    with pytest.raises(ValueError):
        manager.add("", "")


def test_add_non_string_name(manager):
    with pytest.raises(ValueError):
        manager.add(123, "task_description")
    with pytest.raises(ValueError):
        manager.add(123.123, "task_description")
    with pytest.raises(ValueError):
        manager.add(None, "task_description")
    with pytest.raises(ValueError):
        manager.add(True, "task_description")


def test_add_non_string_description(manager):
    with pytest.raises(ValueError):
        manager.add("task_name", 123)
    with pytest.raises(ValueError):
        manager.add("task_name", 123.123)
    with pytest.raises(ValueError):
        manager.add("task_name", None)
    with pytest.raises(ValueError):
        manager.add("task_name", True)


def test_add_non_string_name_and_description(manager):
    with pytest.raises(ValueError):
        manager.add(123, 123)
    with pytest.raises(ValueError):
        manager.add(123.123, 123.123)
    with pytest.raises(ValueError):
        manager.add(None, None)
    with pytest.raises(ValueError):
        manager.add(True, True)


# ---------------------------------------------------------------------
def test_remove_by_id(manager):
    id1 = manager.add("task_name1", "task_description1")
    id2 = manager.add("task_name2", "task_description2")
    id3 = manager.add("task_name3", "task_description3")
    id4 = manager.add("task_name4", "task_description4")

    assert len(manager.get_all()) == 4

    assert manager.remove(id1) is True
    assert manager.remove(id2) is True
    assert manager.remove(id3) is True
    assert manager.remove(id4) is True

    assert manager.get_all() == []


def test_remove_by_id_non_existent(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")
    manager.add("task_name4", "task_description4")
    assert manager.remove(9999) is False


def test_remove_by_id_return_type(manager):
    id1 = manager.add("task_name1", "task_description1")
    assert isinstance(manager.remove(id1), bool)


def test_remove_by_id_empty(manager):
    manager.add("task_name1", "task_description1")
    assert manager.remove(None) is False


def test_remove_by_id_empty_string(manager):
    manager.add("task_name1", "task_description1")
    assert manager.remove("") is False


def test_remove_by_id_negative(manager):
    manager.add("task_name1", "task_description1")
    assert manager.remove(-1) is False
    assert manager.remove(-9999) is False


def test_remove_by_id_float(manager):
    manager.add("task_name1", "task_description1")
    assert manager.remove(1.1) is False
    assert manager.remove(1.5) is False


def test_remove_by_task_name(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")
    manager.add("task_name4", "task_description4")

    assert manager.remove("task_name1") is False
    assert manager.remove("task_name2") is False
    assert manager.remove("task_name3") is False
    assert manager.remove("task_name4") is False


def test_remove_by_task_name_non_existent(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")
    manager.add("task_name4", "task_description4")

    assert manager.remove("task_name5") is False


def test_remove_by_task_description(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")
    manager.add("task_name4", "task_description4")

    assert manager.remove("task_description1") is False
    assert manager.remove("task_description2") is False
    assert manager.remove("task_description3") is False
    assert manager.remove("task_description4") is False


def test_remove_by_task_description_non_existent(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")
    manager.add("task_name4", "task_description4")

    assert manager.remove("task_description5") is False


# ---------------------------------------------------------------------
def test_search_init(manager):
    assert manager.search("task_name") == []


def test_search_by_name(manager):
    id1 = manager.add("task_name1", "task_description1")
    id2 = manager.add("task_name2", "task_description2")
    id3 = manager.add("task_name3", "task_description3")
    id4 = manager.add("task_name4", "task_description4")

    assert manager.search("task_name1") == [
        {
            "id": id1,
            "task_name": "task_name1",
            "task_description": "task_description1",
            "is_finished": False,
        }
    ]
    assert manager.search("task_name2") == [
        {
            "id": id2,
            "task_name": "task_name2",
            "task_description": "task_description2",
            "is_finished": False,
        }
    ]
    assert manager.search("task_name3") == [
        {
            "id": id3,
            "task_name": "task_name3",
            "task_description": "task_description3",
            "is_finished": False,
        }
    ]
    assert manager.search("task_name4") == [
        {
            "id": id4,
            "task_name": "task_name4",
            "task_description": "task_description4",
            "is_finished": False,
        }
    ]


def test_search_by_task_name_non_existent(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")
    manager.add("task_name4", "task_description4")

    assert manager.search("task_name5") == []
    assert manager.search("task_name15087") == []


def test_search_by_description(manager):
    id1 = manager.add("task_name1", "task_description1")
    id2 = manager.add("task_name2", "task_description2")
    id3 = manager.add("task_name3", "task_description3")
    id4 = manager.add("task_name4", "task_description4")

    assert manager.search("task_description1") == [
        {
            "id": id1,
            "task_name": "task_name1",
            "task_description": "task_description1",
            "is_finished": False,
        }
    ]
    assert manager.search("task_description2") == [
        {
            "id": id2,
            "task_name": "task_name2",
            "task_description": "task_description2",
            "is_finished": False,
        }
    ]
    assert manager.search("task_description3") == [
        {
            "id": id3,
            "task_name": "task_name3",
            "task_description": "task_description3",
            "is_finished": False,
        }
    ]
    assert manager.search("task_description4") == [
        {
            "id": id4,
            "task_name": "task_name4",
            "task_description": "task_description4",
            "is_finished": False,
        }
    ]


def test_search_by_task_description_non_existent(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")
    manager.add("task_name4", "task_description4")

    assert manager.search("task_description5") == []
    assert manager.search("task_description15087") == []


def test_search_autocomplete(manager):
    id1 = manager.add("task_name1", "task_description1")
    id2 = manager.add("task_name2", "task_description2")
    id3 = manager.add("task_name3", "task_description3")

    assert manager.search("task_name") == [
        {
            "id": id1,
            "task_name": "task_name1",
            "task_description": "task_description1",
            "is_finished": False,
        },
        {
            "id": id2,
            "task_name": "task_name2",
            "task_description": "task_description2",
            "is_finished": False,
        },
        {
            "id": id3,
            "task_name": "task_name3",
            "task_description": "task_description3",
            "is_finished": False,
        },
    ]


def test_search_autocomplete_non_existent(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")

    assert manager.search("ukol") == []


def test_serach_return_type(manager):
    manager.add("task_name1", "task_description1")
    assert isinstance(manager.search("task_name1"), list)
    assert isinstance(manager.search("task_name1")[0], dict)


# ---------------------------------------------------------------------
def test_list_tasks_empty(manager):
    assert manager.get_all() == []


def test_list_tasks_unfinished(manager):
    id1 = manager.add("task_name1", "task_description1")
    id2 = manager.add("task_name2", "task_description2")
    id3 = manager.add("task_name3", "task_description3")
    id4 = manager.add("task_name4", "task_description4")

    tasks = manager.get_all()
    assert len(tasks) == 4
    assert tasks == [
        {
            "id": id1,
            "task_name": "task_name1",
            "task_description": "task_description1",
            "is_finished": False,
        },
        {
            "id": id2,
            "task_name": "task_name2",
            "task_description": "task_description2",
            "is_finished": False,
        },
        {
            "id": id3,
            "task_name": "task_name3",
            "task_description": "task_description3",
            "is_finished": False,
        },
        {
            "id": id4,
            "task_name": "task_name4",
            "task_description": "task_description4",
            "is_finished": False,
        },
    ]


def test_list_tasks_finished(manager):
    id1 = manager.add("task_name1", "task_description1")
    id2 = manager.add("task_name2", "task_description2")
    id3 = manager.add("task_name3", "task_description3")
    id4 = manager.add("task_name4", "task_description4")

    manager.finish(id1)
    manager.finish(id3)

    tasks = manager.get_all()
    assert len(tasks) == 4
    assert tasks == [
        {
            "id": id1,
            "task_name": "task_name1",
            "task_description": "task_description1",
            "is_finished": True,
        },
        {
            "id": id2,
            "task_name": "task_name2",
            "task_description": "task_description2",
            "is_finished": False,
        },
        {
            "id": id3,
            "task_name": "task_name3",
            "task_description": "task_description3",
            "is_finished": True,
        },
        {
            "id": id4,
            "task_name": "task_name4",
            "task_description": "task_description4",
            "is_finished": False,
        },
    ]


def test_list_tasks_return_type(manager):
    manager.add("task_name1", "task_description1")
    assert isinstance(manager.get_all(), list)
    assert isinstance(manager.get_all()[0], dict)


# ---------------------------------------------------------------------
def test_finish(manager):
    id1 = manager.add("task_name1", "task_description1")
    id2 = manager.add("task_name2", "task_description2")
    id3 = manager.add("task_name3", "task_description3")

    assert manager.finish(id1) is True
    assert manager.finish(id2) is True

    assert manager.search("task_name1") == [
        {
            "id": id1,
            "task_name": "task_name1",
            "task_description": "task_description1",
            "is_finished": True,
        }
    ]
    assert manager.search("task_name2") == [
        {
            "id": id2,
            "task_name": "task_name2",
            "task_description": "task_description2",
            "is_finished": True,
        }
    ]
    assert manager.search("task_name3") == [
        {
            "id": id3,
            "task_name": "task_name3",
            "task_description": "task_description3",
            "is_finished": False,
        }
    ]

    tasks = manager.get_all()
    assert tasks == [
        {
            "id": id1,
            "task_name": "task_name1",
            "task_description": "task_description1",
            "is_finished": True,
        },
        {
            "id": id2,
            "task_name": "task_name2",
            "task_description": "task_description2",
            "is_finished": True,
        },
        {
            "id": id3,
            "task_name": "task_name3",
            "task_description": "task_description3",
            "is_finished": False,
        },
    ]


def test_finish_on_finished_task(manager):
    id1 = manager.add("task_name1", "task_description1")
    manager.finish(id1)
    assert manager.finish(id1) is True


def test_finish_return_type(manager):
    id1 = manager.add("task_name1", "task_description1")
    assert isinstance(manager.finish(id1), bool)


def test_finish_empty(manager):
    manager.add("task_name1", "task_description1")
    assert manager.finish(None) is False


def test_finish_empty_string(manager):
    manager.add("task_name1", "task_description1")
    assert manager.finish("") is False


def test_finish_non_existent(manager):
    manager.add("task_name1", "task_description1")
    assert manager.finish(9999) is False


def test_finish_float(manager):
    manager.add("task_name1", "task_description1")
    assert manager.finish(1.1) is False
    assert manager.finish(1.5) is False


def test_finish_negative(manager):
    manager.add("task_name1", "task_description1")
    assert manager.finish(-1) is False
    assert manager.finish(-9999) is False


# ---------------------------------------------------------------------
def test_clear_all_empty(manager):
    assert manager.get_all() == []
    manager.clear_all()
    assert manager.get_all() == []


def test_clear_all(manager):
    manager.add("task_name1", "task_description1")
    manager.add("task_name2", "task_description2")
    manager.add("task_name3", "task_description3")
    manager.add("task_name4", "task_description4")

    assert len(manager.get_all()) == 4
    manager.clear_all()
    assert len(manager.get_all()) == 0


def test_clear_all_return_type(manager):
    assert isinstance(manager.clear_all(), bool)
