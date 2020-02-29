import tensorflow as tf
import numpy as np
from datetime import datetime
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
load_data=np.loadtxt('./class.csv',delimiter=',')
x_data=load_data[:,0:-1]
t_data=load_data[:,[-1]]
t_data=t_data.astype(np.int32)
t_data1=np.zeros([t_data.shape[0],10])
for i in range(t_data.shape[0]):
    t_data1[i,t_data[i,0]-1]=1
t_data=np.copy(t_data1)
input_nodes=2500
hidden_nodes=100
output_nodes=10
learning_rate = 0.001
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
W5=tf.Variable(tf.random_normal([128*7*7,10],stddev=0.01))
b5=tf.Variable(tf.random_normal([10]))
Z5=logits=tf.matmul(A4_flat,W5)+b5
y=A5=tf.nn.softmax(Z5)

#세션생성
sess=tf.Session()
optimizer=tf.train.AdamOptimizer(learning_rate)
loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=Z5,labels=t))
train=optimizer.minimize(loss)
predicted_val=tf.equal(tf.argmax(A5,1),tf.argmax(t,1))
accuracy=tf.reduce_mean(tf.cast(predicted_val,dtype=tf.float32))
#변수 노드값 초기화
sess.run(tf.global_variables_initializer())
start_time=datetime.now()

for step in range(1000):
    a=np.random.rand(10)*400
    a=a.astype(np.int32)
    loss_val,_=sess.run([loss,train],feed_dict={x:x_data[a],t:t_data[a]})
    
    if step%100==0:
        print('step=',step,', loss=',loss_val)
        accuracy_val=sess.run([accuracy],feed_dict={x:x_data,t:t_data})
        print('\n',accuracy_val)
