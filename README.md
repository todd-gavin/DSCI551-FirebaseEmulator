# DSCI551-FirebaseEmulator

Upload a single file from a specific local director to a specifc directory on EC2:
`scp -i "dsci551-2023.pem" "/Users/toddgavin/Desktop/USC_Classes/DSCI551 - Data Management/GitHub/DSCI551-FirebaseEmulator/code/mongoDBconnect.py" ubuntu@ec2-52-37-233-74.us-west-2.compute.amazonaws.com:/home/ubuntu/FirebaseEmulator/`

## Connect to MongoDB on EC2 instance through shell:
1. Update `mongod.conf` file in directory /etc/. 
    - Run command: `sudo nano mongod.conf`
    - Change bindIP to `bindIp: 127.0.0.1;52.37.233.74;10.26.175.35`

Refer to this Piazza Post: https://piazza.com/class/lcnpg1xru9v6jg/post/413 