# No transport port in front of the hub's byte I/O

After the Frame codec, Poll scheduler and value decoder became pure and host-tested (#2, #6, #7, #8), the hub only moves bytes between the UART, the codec and the scheduler, then publishes decoded Values. A transport port with a UART adapter and a replay adapter would let a whole session run on the host. It would cover only that glue, and it would add an interface the hub doesn't otherwise need. We decided against it (#12). Replay tests feed a raw trace from the Controller (#10) into the codec, the scheduler and the decoder instead.

Revisit this if the hub gains logic of its own that the pure parts don't cover, such as write support or retries that depend on the Values in a Reply.
