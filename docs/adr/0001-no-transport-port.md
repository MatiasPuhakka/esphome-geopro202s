# No transport port in front of the hub's byte I/O

After the Frame codec, Poll scheduler and value decoder became pure and host-tested (#2, #6, #7, #8), the hub only moves bytes between the UART, the codec and the scheduler, then publishes decoded Values. A transport port with a UART adapter and a replay adapter would let a whole session run on the host. It would cover only that glue, and it would add an interface the hub doesn't otherwise need. We decided against it (#12). Replay tests feed a raw trace from the Controller (#10) into the codec and the decoder instead.

Revisit this if the hub gains logic of its own that the pure parts don't cover, such as write support or retries that depend on the Values in a Reply.

## Revisited for #32

The revisit condition held: the hub's `loop()` decides what counts as a Reply, when a request is done and which entity gets each Value, and no host test runs it. The decision stands. The answer is a pure Session module, not a port. The Session takes received bytes and the time and returns Read requests and decoded Values, so a replay of a trace runs the whole loop on the host. The hub stays the only code that touches the UART and `publish_state()`.

A write path (#24) would be a second input to the Session that takes the in-flight slot. It would not add a layer. ADR 0003 still decides whether the Component may write at all.

