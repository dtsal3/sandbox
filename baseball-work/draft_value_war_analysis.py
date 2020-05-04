#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 19:39:56 2017

@author: dtsal
"""
import draft_value_war_pipeline as dvwp

new_big_table = dvwp.ingest_all(1999, 2)

print(new_big_table.groupby('OvPck').WAR.mean())

