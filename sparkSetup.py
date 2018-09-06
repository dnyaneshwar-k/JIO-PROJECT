import config
#import logging
#logger = logging.getLogger('object_detection')
#logger.setLevel(logging.INFO)
import os
import findspark
findspark.init(config.spark_home)

from pyspark import SparkContext, SparkConf

worker = "SPARK_WORKER_INSTANCES=2"

def launch_master():
    out = os.system("sudo $SPARK_HOME/sbin/start-master.sh")
    
    if out == 0:
        print("Spark master is launched [success]")        
    elif out == 256:        
        print("Spark master is already launched [success]") 
    else:        
        print("Spark master launch failed [error]")
        
    return

def launch_slave(): 
    slave = "sudo "+worker+" $SPARK_HOME/sbin/start-slave.sh "+config.spark_master
    out = os.system(slave)
    
    if out == 0:
        print("Spark slaves launched [success]")       
    elif out == 256:        
        print("Spark slaves are already launched [success]")        
    else:        
        print("Spark master launch failed [error]")
        
    return

def start_spark():

    launch_master()
    launch_slave()

def get_spark_context():
    
    conf = SparkConf().setAppName('ObjectDetection').setMaster(config.spark_master)
    
    #conf.set('spark.driver.cores', '4')        
    #conf.set('spark.driver.memory', '2g')
    
    #conf.set('spark.executor.instances','2')
    #conf.set('spark.executor.cores', '1')    
    
    # Kyro Serialsation
    #conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    #conf.set("spark.kryo.registrationRequired", "true")
    #conf.set("spark.kryoserializer.buffer","64m") #Now it's 24 Mb of buffer by default instead of 0.064 Mb
    
    #conf.set("spark.memory.fraction",0.5) #default=0.6 reduce in case of OOM error
    
    #Dynamic allocation
    #conf.set("spark.dynamicAllocation.enabled","true") #default=false, true may cause OOM
    #conf.set("spark.dynamicAllocation.minExecutors","1") #default=0
    #conf.set("spark.dynamicAllocation.maxExecutors","8") #default =infinity
    #conf.set("spark.shuffle.service.enabled", "true") #default=false
       
    #conf.set('spark.default.parallelism', '128') #2 * number of CPUs in total on worker nodes
    #conf.set('spark.driver.supervise','true') #restarts driver automatically if it fails with a non-zero exit status. 
    
    try:
        sc = SparkContext(conf=conf)
        
        # Make Spark logging less extensive
        log4jLogger = sc._jvm.org.apache.log4j
        log_level = log4jLogger.Level.ERROR
        log4jLogger.LogManager.getLogger('org').setLevel(log_level)
    
        return sc
    
    except ValueError as exception:
        print("Could not crearte Spark Context {}".format(exception))

def stop_master():
    status = os.popen("sudo $SPARK_HOME/sbin/spark-daemon.sh status org.apache.spark.deploy.master.Master 1","r").read()
    
    if 'is running' in status:        
        print("Trying to stop master")
        os.system("sudo $SPARK_HOME/sbin/stop-master.sh")
    
    return

def stop_worker():
    status = os.popen("sudo $SPARK_HOME/sbin/spark-daemon.sh status org.apache.spark.deploy.worker.Worker 2","r").read()
    
    if 'is running' in status:
        print("Trying to stop slaves")
        slave = "sudo "+worker+" $SPARK_HOME/sbin/stop-slave.sh "+config.spark_master
        os.system(slave)
    
    status = os.popen("sudo $SPARK_HOME/sbin/spark-daemon.sh status org.apache.spark.deploy.worker.Worker 1","r").read()

    if 'is running' in status:
        print("Trying to stop slaves")
        slave = "sudo "+worker+" $SPARK_HOME/sbin/stop-slave.sh "+config.spark_master
        os.system(slave)
    
    return
        
def stop_spark():
    
    stop_worker()
    stop_master()
                
    status = os.popen("sudo $SPARK_HOME/sbin/spark-daemon.sh status org.apache.spark.deploy.master.Master 1","r").read()
        
    if 'not running' in status:
        print("Spark session successfully stopped")        
    else:
        print("Could not stop spark")
