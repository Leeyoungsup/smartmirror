import cv2
import csv
import glob
import tensorflow as tf
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
def Imagecapture(classcount):
    cap = cv2.VideoCapture(0)
    count=0
    while(count<400):
        ret, frame = cap.read() 
        dst = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dst = cv2.resize(dst, (50,50), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('class'+str(classcount)+'/'+str(count)+'.jpg',dst)
        count=count+1
    cap.release()
    cv2.destroyAllWindows()
def Image_recognition():
    cap = cv2.VideoCapture(0)
    count=0
    while(count<1):
        ret, frame = cap.read() 
        dst = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dst = cv2.resize(dst, (50,50), interpolation=cv2.INTER_CUBIC)
        imsi=dst.reshape(1,2500)
        count+=1
    cap.release()
    cv2.destroyAllWindows()
    return imsi
f = open('class.csv', 'w', encoding='utf-8',newline='')
wr = csv.writer(f)
while(True):
    a=input(':')
    if a=='1':
        Imagecapture(1)
    if a=='2':
        Imagecapture(2)
    if a=='3':
        Imagecapture(3)
    if a=='4':
        Imagecapture(4)
    if a=='q':
        break
    
        
    if a=='p':
        print('학습시작')
        for j in range(4):
            images = glob.glob('Class'+str(j+1)+'/*.jpg')
            for i in range(400):
                imsi=cv2.imread(images[i], cv2.IMREAD_ANYCOLOR)
                imsi=imsi.reshape(1,2500)
                imsi=np.append(imsi,j+1)
                imsi=imsi.reshape(1,2501)
                wr.writerow(imsi[0])
        load_data=np.loadtxt('./class.csv',delimiter=',')
        x_data=load_data[:,0:-1]
        t_data=load_data[:,[-1]]
        t_data=t_data.astype(np.int32)
        t_data1=np.zeros([t_data.shape[0],4])
        for i in range(t_data.shape[0]):
            t_data1[i,t_data[i,0]-1]=1
        t_data=np.copy(t_data1)
        input_nodes=2500
        hidden_nodes=100
        output_nodes=4
        learning_rate = 0.1
        epochs = 1
        batch_size = 100 
        x=tf.placeholder(tf.float32,[None,input_nodes])
        t=tf.placeholder(tf.float32,[None,output_nodes])
        A1=X_img=tf.reshape(x,[-1,50,50,1])
        #필터 32개
        F2=tf.Variable(tf.random_normal([3,3,1,32],stddev=0.01))
        b2=tf.Variable(tf.constant(0.1,shape=[32]))
        #컨벌루션 연산 28,28,1->28,28,32
        C2=tf.nn.conv2d(A1,F2,strides=[1,1,1,1],padding='SAME')
        Z2=tf.nn.relu(C2+b2)
        #max pooling 28,28,32->14,14,32
        A2=P2=tf.nn.max_pool(Z2,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
        #필터 64개
        F3=tf.Variable(tf.random_normal([3,3,32,64],stddev=0.01))
        b3=tf.Variable(tf.constant(0.1,shape=[64]))
        #컨벌루션 연산 14,14,32->14,14,64
        C3=tf.nn.conv2d(A2,F3,strides=[1,1,1,1],padding='SAME')
        Z3=tf.nn.relu(C3+b3)
        #max pooling 14,14,64->7,7,64
        A3=P3=tf.nn.max_pool(Z3,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
        #필터 128개
        F4=tf.Variable(tf.random_normal([3,3,64,128],stddev=0.01))
        b4=tf.Variable(tf.constant(0.1,shape=[128]))
        #컨벌루션 연산 7,7,64->7,7,128
        C4=tf.nn.conv2d(A3,F4,strides=[1,1,1,1],padding='SAME')
        Z4=tf.nn.relu(C4+b4)
        #max pooling 7,7,128->4,4,128
        A4=P4=tf.nn.max_pool(Z4,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
        #1차원 벡터로 변경
        A4_flat=P4_flat=tf.reshape(A4,[-1,128*7*7])
        hidden_node=20
        W5=tf.Variable(tf.random_normal([128*7*7,hidden_node],stddev=0.01))
        b5=tf.Variable(tf.random_normal([hidden_node]))
        Z5=logits=tf.matmul(A4_flat,W5)+b5
        A5=tf.nn.relu(Z5)
        W6=tf.Variable(tf.random_normal([hidden_node,4],stddev=0.01))
        b6=tf.Variable(tf.random_normal([4]))
        Z6=logits=tf.matmul(A5,W6)+b6
        y=A6=tf.nn.softmax(Z6)
        
        #세션생성
        sess=tf.Session()
        optimizer=tf.train.AdamOptimizer(learning_rate)
        loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=Z6,labels=t))
        train=optimizer.minimize(loss)
        predicted_val=tf.equal(tf.argmax(A6,1),tf.argmax(t,1))
        accuracy=tf.reduce_mean(tf.cast(predicted_val,dtype=tf.float32))
        #변수 노드값 초기화
        sess.run(tf.global_variables_initializer())
        
        for step in range(1000):
            a=np.random.rand(10)*1600
            a=a.astype(np.int32)
            loss_val,_=sess.run([loss,train],feed_dict={x:x_data[a],t:t_data[a]})
            
            if step%100==0:
                print('step=',step,', loss=',loss_val)
                accuracy_val=sess.run([accuracy],feed_dict={x:x_data,t:t_data})
                print('\n',accuracy_val)
    if a=='o':
        for i in range(10):
            x_data=Image_recognition()
            k=sess.run([tf.argmax(A6,1)+1],feed_dict={x:x_data})
            print(k[0][0])