from kombu import Exchange, Queue

from classic.messaging_kombu import BrokerScheme

broker_scheme_publ = BrokerScheme(
    Queue('book', Exchange('book'))
)

broker_scheme_cons = BrokerScheme(
    Queue('user', Exchange('user'))
)
