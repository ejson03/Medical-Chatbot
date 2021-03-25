from rasa.core.tracker_store import TrackerStore
from rasa.core.domain import Domain
from typing import Iterator, Optional, Text, Iterable, Union, Dict
from rasa.core.brokers.event_channel import EventChannel
from rasa.core.trackers import ActionExecuted, DialogueStateTracker, EventVerbosity

class NeoTrackerStore(TrackerStore):
    """Stores conversation history"""

    def __init__(
        self, domain: Domain,url: Optional[str] = None, event_broker: Optional[EventChannel] = None
    ) -> None: 
        self.store = {}
        super(NeoTrackerStore, self).__init__(domain, event_broker)

    # def init_tracker(self, sender_id):
    #     if self.domain:
    #         return DialogueStateTracker(sender_id,
    #                                 self.domain.slots,
    #                                 max_event_history = 1)
    #     else:
    #         return None

    def save(self, tracker: DialogueStateTracker) -> None:
        """Updates and saves the current conversation state"""
        if self.event_broker:
            self.stream_events(tracker)

        ## get the current state data from tracker
        state = tracker.current_state(EventVerbosity.APPLIED)
        print("#"*50)
        print(state.get("events"))
        print("#"*50)

        serialised = NeoTrackerStore.serialise_tracker(tracker)
        self.store[tracker.sender_id] = serialised
       
    def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        """
        Args:
            sender_id: the message owner ID
        Returns:
            DialogueStateTracker
        """
        if sender_id in self.store:
            return self.deserialise_tracker(sender_id, self.store[sender_id])
        else:
            return None


    def keys(self) -> Iterable[Text]:
        """Returns sender_ids of the Tracker Store"""
        return self.store.keys()

    