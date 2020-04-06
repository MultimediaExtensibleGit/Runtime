import pytest
import os
from meg_runtime.locking.lockFile import LockFile



@pytest.fixture()
def generateLockfile():
    fileName = ".meg/templockfile"
    try:
        os.mkdir(".meg")
    except FileExistsError:
        pass
    try:
        tempFile = LockFile(fileName)
        yield fileName
    finally:
        os.remove(fileName)
        os.rmdir(".meg")

def test_load(generateLockfile):
    lock = LockFile(generateLockfile)
    lock.addLock("project/jeffsPart.dwg", "jeff")
    try:
        lock.load("emptyFile")
        assert len(lock.locks) == 0
    finally:
        os.remove("emptyFile")

def test_locks(generateLockfile):
    lock = LockFile(generateLockfile)
    lock.addLock("project/jeffsPart.dwg", "jeff")
    lock.addLock("project/jeffs2ndPart.dwg", "jeff")
    with pytest.raises(AttributeError):
        lock.locks = None
    assert len(lock.locks) == 2

def test_addLock(generateLockfile):
    lock = LockFile(generateLockfile)
    lock.addLock("project/jeffsPart.dwg", "jeff")
    lock.addLock("project/jeffs2ndPart.dwg", "bob")
    assert lock.locks[0]["file"] == "project/jeffsPart.dwg"
    assert lock.locks[0]["user"] == "jeff"
    assert lock.locks[1]["file"] == "project/jeffs2ndPart.dwg"
    assert lock.locks[1]["user"] == "bob"

def test_removeLock(generateLockfile):
    lock = LockFile(generateLockfile)
    lock.addLock("project/jeffsPart.dwg", "jeff")
    lock.addLock("project/jeffs2ndPart.dwg", "bob")
    lock.removeLock("project/jeffsPart.dwg")
    lock.removeLock("nonExistantLock") #should not error
    assert len(lock.locks) == 1
    assert lock.locks[0]["file"] == "project/jeffs2ndPart.dwg"

def test_findLock(generateLockfile):
    lock = LockFile(generateLockfile)
    lock.addLock("project/jeffsPart.dwg", "jeff")
    lock.addLock("project/jeffs2ndPart.dwg", "bob")
    entry = lock.findLock("project/jeffs2ndPart.dwg")
    assert entry["file"] == "project/jeffs2ndPart.dwg"
    assert entry["user"] == "bob"