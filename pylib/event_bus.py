
def foo():
    print __name__
print __name__

import traceback

class event_bus_t(object):
    def __init__(self):
        #key event class, value is dict of consumer function
        self.event_consumer = {}
        #processing list, cache event
        self.event_cache_list = []#fifo
        def default_except_handler(exception_):
            traceback.print_exc()
        self.exception_handler = default_except_handler
    def set_exception_handler(func_):
        self.exception_handler = func_
    def get_key_name(self, event_obj_):
        return event_obj_.__class__
    def bind_event(self, event_class_, consumer_func):
        key = event_class_
        consumer_name = consumer_func.__module__ + '.' + consumer_func.__name__
        dest_dict = self.event_consumer.get(key)
        if dest_dict == None:
            dest_dict = {}
            self.event_consumer[key] = dest_dict
        dest_dict[consumer_name] = consumer_func
    def post(self, event_):
        self.event_cache_list.insert(0, event_)
        size = len(self.event_cache_list)
        if size > 1:
            return True

        while len(self.event_cache_list) > 0:
            next_event = self.event_cache_list[len(self.event_cache_list) - 1]
            key = self.get_key_name(next_event)
            dest_dict = self.event_consumer.get(key)
            if None != dest_dict:
                for k, func in dest_dict.iteritems():
                    try:
                        func(event_)
                    except Exception, e:
                        self.exception_handler(e)
                    except:
                        pass
            self.event_cache_list.pop()

    def dump(self):
        print(self.event_consumer)

event_bus = event_bus_t()
def get_event_bus():
    return event_bus

def bind_event(event_class_):
    def wraper(func_):
        ebus = get_event_bus()
        ebus.bind_event(event_class_, func_)
        return func_
    return wraper

class test_event_t(object):
    pass
class test_event2_t(object):
    pass


@bind_event(test_event_t)
def process_test_event(event_):
    get_event_bus().post(test_event2_t())
    print(__name__, 'process_test_event OhNice!!!')
    get_event_bus().post(test_event2_t())
@bind_event(test_event2_t)
def process_test_event2(event_):
    print(__name__, 'process_test_event2 OhNice!!!', event_)


event_bus.dump()
test_event = test_event_t()

event_bus.post(test_event)

process_test_event2('')
