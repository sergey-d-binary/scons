__revision__ = "JobTests.py __REVISION__ __DATE__ __DEVELOPER__"

import unittest
import random
import math
import scons.Job
import sys

# a large number
num_sines = 10000

# how many parallel jobs to perform for the test
num_jobs = 11

# how many tasks to perform for the test
num_tasks = num_jobs*5

class DummyLock:
    "fake lock class to use if threads are not supported"
    def acquire(self):
        pass

    def release(self):
        pass

class NoThreadsException:
    "raised by the ParallelTestCase if threads are not supported"

    def __str__(self):
        return "the interpreter doesn't support threads"

class Task:
    """A dummy task class for testing purposes."""

    def __init__(self, i, taskmaster):
        self.i = i
        self.taskmaster = taskmaster
        self.was_executed = 0
        
    def execute(self):
        self.taskmaster.guard.acquire()
        self.taskmaster.begin_list.append(self.i)
        self.taskmaster.guard.release()

        # do something that will take some random amount of time:
        for i in range(random.randrange(0, num_sines, 1)):
            x = math.sin(i)

        self.was_executed = 1

        self.taskmaster.guard.acquire()
        self.taskmaster.end_list.append(self.i)
        self.taskmaster.guard.release()

class ExceptionTask:
    """A dummy task class for testing purposes."""

    def __init__(self, i, taskmaster):
        pass
        
    def execute(self):
        raise "exception"

class Taskmaster:
    """A dummy taskmaster class for testing the job classes."""

    def __init__(self, n, test_case, Task):
        """n is the number of dummy tasks to perform."""

        self.test_case = test_case
        self.num_tasks = n
        self.num_iterated = 0
        self.num_executed = 0
        self.num_failed = 0
        self.Task = Task
        # 'guard' guards 'task_begin_list' and 'task_end_list'
        try:
            import threading
            self.guard = threading.Lock()
        except:
            self.guard = DummyLock()

        # keep track of the order tasks are begun in
        self.begin_list = []

        # keep track of the order tasks are completed in
        self.end_list = []


    def next_task(self):
        if self.all_tasks_are_iterated():
            return None
        else:
            self.num_iterated = self.num_iterated + 1
            return self.Task(self.num_iterated, self)

    def all_tasks_are_executed(self):
        return self.num_executed == self.num_tasks

    def all_tasks_are_iterated(self):
        return self.num_iterated == self.num_tasks

    def executed(self, task):
        self.num_executed = self.num_executed + 1

        self.test_case.failUnless(task.was_executed,
                                  "the task wasn't really executed")
        self.test_case.failUnless(task.__class__ is Task,
                                  "the task wasn't really a Task instance")

    def failed(self, task):
        self.num_failed = self.num_failed + 1
    
    def is_blocked(self):
        # simulate blocking tasks
        return self.num_iterated - self.num_executed >= max(num_jobs/2, 2)

    def tasks_were_serial(self):
        "analyze the task order to see if they were serial"
        serial = 1 # assume the tasks were serial
        for i in range(num_tasks):
            serial = serial and (self.begin_list[i]
                                 == self.end_list[i]
                                 == (i + 1))
        return serial

class ParallelTestCase(unittest.TestCase):
    def runTest(self):
        "test parallel jobs"
        
        try:
            import threading
        except:
            raise NoThreadsException()

        taskmaster = Taskmaster(num_tasks, self, Task)
        jobs = scons.Job.Jobs(num_jobs, taskmaster)
        jobs.start()
        jobs.wait()

        self.failUnless(not taskmaster.tasks_were_serial(),
                        "the tasks were not executed in parallel")
        self.failUnless(taskmaster.all_tasks_are_executed(),
                        "all the tests were not executed")
        self.failUnless(taskmaster.all_tasks_are_iterated(),
                        "all the tests were not iterated over")
        self.failIf(taskmaster.num_failed,
                    "some task(s) failed to execute") 

class SerialTestCase(unittest.TestCase):
    def runTest(self):
        "test a serial job"

        taskmaster = Taskmaster(num_tasks, self, Task)
        jobs = scons.Job.Jobs(1, taskmaster)
        jobs.start()
        jobs.wait()

        self.failUnless(taskmaster.tasks_were_serial(),
                        "the tasks were not executed in series")
        self.failUnless(taskmaster.all_tasks_are_executed(),
                        "all the tests were not executed")
        self.failUnless(taskmaster.all_tasks_are_iterated(),
                        "all the tests were not iterated over")
        self.failIf(taskmaster.num_failed,
                    "some task(s) failed to execute") 

class SerialExceptionTestCase(unittest.TestCase):
    def runTest(self):
        "test a serial job with tasks that raise exceptions"

        taskmaster = Taskmaster(num_tasks, self, ExceptionTask)
        jobs = scons.Job.Jobs(1, taskmaster)
        jobs.start()
        jobs.wait()

        self.failIf(taskmaster.num_executed,
                    "a task was executed")
        self.failUnless(taskmaster.num_iterated == 1,
                    "exactly one task should have been iterated")
        self.failUnless(taskmaster.num_failed == 1,
                    "exactly one task should have failed")

class ParallelExceptionTestCase(unittest.TestCase):
    def runTest(self):
        "test parallel jobs with tasks that raise exceptions"

        taskmaster = Taskmaster(num_tasks, self, ExceptionTask)
        jobs = scons.Job.Jobs(num_jobs, taskmaster)
        jobs.start()
        jobs.wait()

        self.failIf(taskmaster.num_executed,
                    "a task was executed")
        self.failUnless(taskmaster.num_iterated >= 1,
                    "one or more task should have been iterated")
        self.failUnless(taskmaster.num_failed >= 1,
                    "one or more tasks should have failed") 


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ParallelTestCase())
    suite.addTest(SerialTestCase())
    suite.addTest(SerialExceptionTestCase())
    suite.addTest(ParallelExceptionTestCase())
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    result = runner.run(suite())
    if (len(result.failures) == 0
        and len(result.errors) == 1
        and type(result.errors[0][0]) == SerialTestCase
        and type(result.errors[0][1][0]) == NoThreadsException):
        sys.exit(2)
    elif not result.wasSuccessful():
        sys.exit(1)

            

        
    
    
    
    


