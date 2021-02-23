import os
import time

import tensorflow as tf
import numpy as np

config = tf.ConfigProto(allow_soft_placement=True)
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
config.gpu_options.allow_growth = True


def read_file(path, read_header=False):
    f = open(path, "r+")
    rows = f.readlines()
    if not read_header:
        rows = rows[1:]
    cols = []
    for row in rows:
        col = str.split(row)
        if len(col) == 1:
            cols.append([float(col[0])])
        else:
            cols.append([float(c) for c in col])
    return cols


def write_file(path, header, data):
    f = open(path, "w+")
    if header is not None:
        row = ""
        for h in header:
            row += "\t" + h
        row = row[1:] + "\n"
        f.write(row)
    for cols in data:
        row = ""
        for col in cols:
            row += "\t" + '{:e}'.format(col)
        row = row[1:] + "\n"
        f.write(row)
    f.close()


def multilayer_perceptron(x, weight, bias):
    l1 = tf.add(tf.matmul(x, weight['h1']), bias['h1'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, weight['h2']), bias['h2'])
    l2 = tf.nn.relu(l2)

    out = tf.add(tf.matmul(l2, weight['out']), bias['out'])
    out = tf.nn.relu(out)

    return out


def train(train_data_path, train_label_path, model_path, log_path, batch_size, epochs, learning_rate, decay_rate,
          staircase, reload_path=""):
    x = tf.placeholder('float', [None, 3])
    y = tf.placeholder('float', [None, 1])

    weight = {
        'h1': tf.Variable(tf.random_normal([3, 4])),
        'h2': tf.Variable(tf.random_normal([4, 4])),
        'out': tf.Variable(tf.random_normal([4, 1]))
    }

    bias = {
        'h1': tf.Variable(tf.random_normal([4])),
        'h2': tf.Variable(tf.random_normal([4])),
        'out': tf.Variable(tf.random_normal([1]))
    }

    # with tf.Graph().as_default():
    with tf.Session(config=config) as sess:
        """global step"""
        global_step = tf.Variable(0, name="global_step", trainable=False)

        pred = multilayer_perceptron(x, weight, bias)
        loss = tf.reduce_mean(tf.abs(tf.subtract(pred, y)))
        # decay learning rate
        lr = tf.train.exponential_decay(learning_rate, global_step=global_step,
                                        decay_steps=10000, decay_rate=decay_rate, staircase=staircase)
        optimizer = tf.train.AdamOptimizer(lr).minimize(loss=loss, global_step=global_step)

        """calculate accuracy"""
        correct_prediction = tf.subtract(tf.constant(1, dtype=tf.float32),
                                         tf.divide(tf.abs(tf.subtract(pred, y)), y))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float'))

        if not os.path.exists(model_path):
            os.mkdir(model_path)
        model_path = model_path + "/" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) \
                     + "_epoch-" + str(epochs) + "_batch-" + str(batch_size) \
                     + "_lr-" + str(learning_rate) + "_dr-" + str(decay_rate) \
                     + "_staircase-" + str(staircase)
        if not os.path.exists(model_path):
            os.mkdir(model_path)

        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_path = log_path + "/" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) \
                   + "_epoch-" + str(epochs) + "_batch-" + str(batch_size) \
                   + "_lr-" + str(learning_rate) + "_dr-" + str(decay_rate) \
                   + "_staircase-" + str(staircase)
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        info = 'lr=%f, dr=%f, staircase=%s, epoch=%d, batch_size=%d' % (
            learning_rate, decay_rate, staircase, epochs, batch_size)
        all_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)

        """summary"""
        tf.summary.scalar("loss", loss)
        tf.summary.scalar("accuracy", accuracy)
        tf.summary.scalar("learning_rate", lr)
        tf.summary.histogram("weight h1", weight['h1'])
        tf.summary.histogram("weight h2", weight['h2'])
        tf.summary.histogram("weight out", weight['out'])
        tf.summary.histogram("bias h1", bias['h1'])
        tf.summary.histogram("bias h2", bias['h2'])
        tf.summary.histogram("bias out", bias['out'])

        """read data from txt"""
        data = read_file(train_data_path, read_header=False)
        data = np.array(data)
        label = read_file(train_label_path, read_header=False)
        label = np.array(label)
        print("read data: ", data.shape)
        print("read label:", label.shape)

        """using tf.data.Dataset feed data into model"""
        dataset = tf.data.Dataset.from_tensor_slices((data, label))
        dataset = dataset.shuffle(buffer_size=256).batch(batch_size=batch_size).repeat()
        iterator = dataset.make_one_shot_iterator()
        one_element = iterator.get_next()

        batch_total = int(data.shape[0] / batch_size) + 1

        sess.run(tf.global_variables_initializer())
        # write summary
        merged = tf.summary.merge_all()
        text_summary = tf.summary.text("info", tf.convert_to_tensor(info))
        summary_writer = tf.summary.FileWriter(log_path, sess.graph)
        summary = sess.run(text_summary)
        summary_writer.add_summary(summary, 0)
        # saver
        saver = tf.train.Saver(all_vars, max_to_keep=3)
        if reload_path != "":
            ckpt = tf.train.get_checkpoint_state(reload_path)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                print("restore and continue training!")
            else:
                pass

        start_time = time.time()
        step = sess.run(global_step)
        for i in range(epochs):
            for j in range(batch_total):
                x_batch, y_batch = sess.run(one_element)

                _, summary_train = sess.run([optimizer, merged], feed_dict={x: x_batch, y: y_batch})
                summary_writer.add_summary(summary_train, step)

                if step % 100 == 0:
                    duration = time.time() - start_time
                    print('%d steps, spend %.3f sec' % (step, duration))
                    start_time = time.time()
                if step % 1000 == 0:
                    save_path = saver.save(sess, os.path.join(model_path, "model.ckpt"),
                                           global_step=global_step)
                    print("Model saved in file: %s" % save_path)
                step = sess.run(global_step)
        save_path = saver.save(sess, os.path.join(model_path, "model.ckpt"), global_step=global_step)
        print("Finished! Model saved in file: %s" % save_path)
        sess.close()


def test(test_data, model_path):
    x = tf.placeholder('float', [1, 3])
    y = tf.placeholder('float', [1, 1])

    weight = {
        'h1': tf.Variable(tf.random_normal([3, 4])),
        'h2': tf.Variable(tf.random_normal([4, 4])),
        'out': tf.Variable(tf.random_normal([4, 1]))
    }

    bias = {
        'h1': tf.Variable(tf.random_normal([4])),
        'h2': tf.Variable(tf.random_normal([4])),
        'out': tf.Variable(tf.random_normal([1]))
    }

    out_list = []

    with tf.Session(config=config) as sess:
        pred = multilayer_perceptron(x, weight, bias)

        """read data from txt"""
        data = read_file(test_data, read_header=False)
        data = np.array(data)
        print("read test data: ", data.shape)

        sess.run(tf.global_variables_initializer())

        # saver
        saver = tf.train.Saver(tf.global_variables(), write_version=tf.train.SaverDef.V1)
        ckpt = tf.train.get_checkpoint_state(model_path)
        saver.restore(sess, ckpt.model_checkpoint_path)

        for row in data:
            row = np.expand_dims(row, axis=0)
            output = sess.run(pred, feed_dict={x: row})
            out_list.append(output[0])
        sess.close()
    return out_list


def main(training=True):
    if training:
        train_data = "./train_data.txt"
        train_truth = "./train_truth.txt"
        model_path = "./model"
        log_path = "./log"
        train(train_data, train_truth, model_path, log_path,
              batch_size=8,
              epochs=50,
              learning_rate=1e-3,
              decay_rate=0.99,
              reload_path="./model/20210219_093100_epoch-50_batch-16_lr-0.001_dr-0.99_staircase-True",
              staircase=True)
    else:
        test_data = "./test_data.txt"
        output_path = "./test_predicted.txt"
        model_path = "./model/20210219_100653_epoch-50_batch-4_lr-0.001_dr-0.98_staircase-True"
        output = test(test_data, model_path)
        output = np.reshape(output, (-1, 1))
        write_file(output_path, ["y"], output)


if __name__ == '__main__':
    main(training=False)
