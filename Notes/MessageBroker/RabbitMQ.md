# RabbitMQ

* [RabbitMQ Tutorials | RabbitMQ](https://www.rabbitmq.com/tutorials)

```bash
sudo apt install rabbitmq-server
sudo systemctl status rabbitmq-server

sudo rabbitmqctl list_queues
sudo rabbitmq-diagnostics -q ping
```

Tutorial

* [RabbitMQ Tutorials | RabbitMQ](https://www.rabbitmq.com/tutorials)
    1. [RabbitMQ tutorial - "Hello world!" | RabbitMQ](https://www.rabbitmq.com/tutorials/tutorial-one-python)
    2. [RabbitMQ tutorial - Work Queues | RabbitMQ](https://www.rabbitmq.com/tutorials/tutorial-two-python)
       * `ack` is a must have ([Consumer Acknowledgements and Publisher Confirms | RabbitMQ](https://www.rabbitmq.com/docs/confirms))
       * To ensure round-robin dispatching is fair we can use `channel.basic_qos(prefetch_count=1)`
    3. [RabbitMQ tutorial - Publish/Subscribe | RabbitMQ](https://www.rabbitmq.com/tutorials/tutorial-three-python)
       * `exchange`
    4. [RabbitMQ tutorial - Routing | RabbitMQ](https://www.rabbitmq.com/tutorials/tutorial-four-python)
    5. [RabbitMQ tutorial - Topics | RabbitMQ](https://www.rabbitmq.com/tutorials/tutorial-five-python)
    6. [RabbitMQ tutorial - Remote procedure call (RPC) | RabbitMQ](https://www.rabbitmq.com/tutorials/tutorial-six-python)
* [RabbitMQ tutorial - "Hello World!" (Stream) | RabbitMQ](https://www.rabbitmq.com/tutorials/tutorial-one-python-stream)


## Python Client

* [Clients Libraries and Developer Tools | RabbitMQ](https://www.rabbitmq.com/client-libraries/devtools#python-dev)

Pika

* [pika/pika: Pure Python RabbitMQ/AMQP 0-9-1 client library](https://github.com/pika/pika)
* [Introduction to Pika — pika 1.3.2 documentation](https://pika.readthedocs.io/en/stable/)

rabbitpy

* [gmr/rabbitpy: A pure python, thread-safe, minimalistic and pythonic RabbitMQ client library](https://github.com/gmr/rabbitpy)
* [rabbitpy: RabbitMQ Simplified — rabbitpy 2.0.1 documentation](https://rabbitpy.readthedocs.io/en/latest/)

---

* [Part 2.3: Getting started with RabbitMQ and Python - CloudAMQP](https://www.cloudamqp.com/blog/part2-3-rabbitmq-for-beginners_example-and-sample-code-python.html)
* [Python Documentation - CloudAMQP](https://www.cloudamqp.com/docs/python.html)
