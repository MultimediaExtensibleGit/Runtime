import pytest
from unittest import mock
import os
import meg_runtime.locking as locking
from meg_runtime.locking.lockFile import LockFile

TOTAL_LOCKS_INITALIZED = 3

@pytest.fixture()
def generateLocking():
    try:
        os.mkdir(".meg")
    except FileExistsError:
        pass
    try:
        lock = LockFile(locking.LOCKFILE_DIR + locking.LOCKFILE_NAME)
        lock.addLock("project/jeffsPart.dwg", "jeff")
        lock.addLock("project/jeffs2ndPart.dwg", "bob")
        lock.addLock("src/other.txt", "bob")
        lock.save()
        yield locking.LockingManager("bob", mock.MagicMock(), mock.MagicMock())
    finally:
        os.remove(locking.LOCKFILE_DIR + locking.LOCKFILE_NAME)
        os.rmdir(".meg")

def test_locks(generateLocking):
    with pytest.raises(AttributeError):
        generateLocking.locks = None
    assert len(generateLocking.locks) == TOTAL_LOCKS_INITALIZED

def test_findLock(generateLocking):
    entry = generateLocking.findLock("project/jeffs2ndPart.dwg")
    assert entry["file"] == "project/jeffs2ndPart.dwg"
    assert entry["user"] == "bob"
    entry = generateLocking.findLock("project/jeffsPart.dwg")
    assert entry["file"] == "project/jeffsPart.dwg"
    assert entry["user"] == "jeff"
    assert generateLocking.findLock("IOEFJIOFIJEFIOEFJIOEFJIKOEFJOIKEFKOPEFOPKEF") is None

def test_addLock(generateLocking):
    assert generateLocking.addLock("project/jeffs2ndPart.dwg") == False #Lock belonging to local user else already exists
    assert generateLocking.addLock("project/jeffsPart.dwg") == False #Lock belonging to someone else already exists
    assert generateLocking.addLock("morethings/aThing.svg") == True
    assert generateLocking.findLock("morethings/aThing.svg")["user"] == "bob"

def test_removeLock(generateLocking):
    assert generateLocking.removeLock("project/jeffsPart.dwg") == False #Lock belonging to someone else
    assert generateLocking.removeLock("src/other.txt") == True
    assert len(generateLocking.locks) == TOTAL_LOCKS_INITALIZED - 1

