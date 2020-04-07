import pytest
import os
from meg_runtime.locking.lockFile import LockFile


@pytest.fixture()
def generateLockfile():
    fileName = ".meg/templockfile"
    try:
        tempFile = LockFile(fileName)
        yield fileName
    finally:
        os.remove(fileName)
        os.rmdir(".meg")

def test_load(generateLockfile):
    lock = LockFile(generateLockfile)
    lock["project/jeffsPart.dwg"] = "jeff"
    try:
        lock.load("./emptyFile")
        assert len(lock) == 0
    finally:
        os.remove("emptyFile")

def test_locks(generateLockfile):
    lock = LockFile(generateLockfile)
    lock["project/jeffsPart.dwg"] = "jeff"
    lock["project/jeffs2ndPart.dwg"] = "jeff"
    assert len(lock) == 2

def test_addLock(generateLockfile):
    lock = LockFile(generateLockfile)
    lock["project/jeffsPart.dwg"] = "jeff"
    lock["project/jeffs2ndPart.dwg"] = "bob"
    assert lock["project/jeffsPart.dwg"]["user"] == "jeff"
    assert lock["project/jeffs2ndPart.dwg"]["user"] == "bob"

def test_removeLock(generateLockfile):
    lock = LockFile(generateLockfile)
    lock["project/jeffsPart.dwg"] = "jeff"
    lock["project/jeffs2ndPart.dwg"] = "bob"
    del lock["project/jeffsPart.dwg"]
    del lock["nonExistantLock"] #should not error
    assert len(lock) == 1
    assert not lock["project/jeffs2ndPart.dwg"] is None 

def test_findLock(generateLockfile):
    lock = LockFile(generateLockfile)
    lock["project/jeffsPart.dwg"] = "jeff"
    lock["project/jeffs2ndPart.dwg"] = "bob"
    entry = lock["project/jeffs2ndPart.dwg"]
    assert entry["user"] == "bob"