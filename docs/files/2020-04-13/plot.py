#!/usr/bin/env python3

import argparse
import json
import pandas as pd

import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Plots test results.")
parser.add_argument('test', type=str,
        help="The name of the test to plot.")
parser.add_argument('-o', '--output', type=str,
        help="Sets output file base name.")
parser.add_argument('-e', '--output-extension', type=str, default="png",
        help="Sets the extension for output files (i.e. pdf, png, etc.).")
args = parser.parse_args()


def openStreams(fname):
    with open(fname) as fin:
        data = json.load(fin)

    streams = [i['streams'] for i in data['intervals']]
    streams = list(zip(*streams))
    streams = [pd.DataFrame(s) for s in streams]

    return streams


clientStreams = openStreams(args.test + "_client.json")
serverStreams = openStreams(args.test + "_server.json")


mpl.style.use('seaborn-bright')
mpl.rc('figure', dpi=200)


### Rate ###
fig = plt.figure()
ax = fig.add_subplot(111)

for i, strm in enumerate(serverStreams):
    ax.plot(strm.start, strm.bits_per_second/2**20, label=f"Stream {i}")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Rate (Mbps)")
ax.set_ylim(-5, 1000)
ax.legend()

if args.output is not None:
    plt.savefig(f"{args.output}-rate.{args.output_extension}", bbox_inches='tight')


### cwnd ###
fig = plt.figure()
ax = fig.add_subplot(111)

for i, strm in enumerate(clientStreams):
    ax.plot(strm.start, strm.snd_cwnd/2**20, label=f"Stream {i}")

ax.set_xlabel("Time (s)")
ax.set_ylabel("CWND (Mbits)")
ax.legend()

if args.output is not None:
    plt.savefig(f"{args.output}-cwnd.{args.output_extension}", bbox_inches='tight')


### RTT ###
fig = plt.figure()
ax = fig.add_subplot(111)

for i, strm in enumerate(clientStreams):
    ax.plot(strm.start, strm.rtt/1e3, label=f"Stream {i}")

ax.set_xlabel("Time (s)")
ax.set_ylabel("RTT (ms)")
ax.legend()

if args.output is not None:
    plt.savefig(f"{args.output}-rtt.{args.output_extension}", bbox_inches='tight')


## Losses
fig = plt.figure()
ax = fig.add_subplot(111)

for i, strm in enumerate(clientStreams):
    ax.plot(strm.start, strm.retransmits, label=f"Stream {i}")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Losses")
ax.legend()

if args.output is not None:
    plt.savefig(f"{args.output}-losses.{args.output_extension}", bbox_inches='tight')


if args.output is None:
    plt.show()
