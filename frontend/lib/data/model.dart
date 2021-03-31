import 'package:rabbit_messenger_frontend/data/channels.dart';
import 'package:rabbit_messenger_frontend/data/users.dart';
import 'package:sqfentity_gen/sqfentity_gen.dart';

import 'package:sqfentity/sqfentity.dart';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
part 'model.g.dart';

@SqfEntityBuilder(dbModel)
const dbModel = SqfEntityModel(
  databaseName: "RabbitMessengerOperational.db",
  bundledDatabasePath: "assets/operational.sqlite",
  databaseTables: [usersTable, channelsTable],
);