import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import './channels.dart';

class Users extends StatelessWidget {
  final int amount;
  final EmptyReturnCallback callback;

  Users(this.amount, this.callback);

  @override
  Widget build(BuildContext context) {
    return Scrollbar(
      child: ListView.builder(
          itemCount: amount,
          itemBuilder: (context, num) {
            return Container(
              decoration: BoxDecoration(
                  color: Colors.white70,
                  border: Border(
                      bottom:
                          BorderSide(color: Theme.of(context).dividerColor))),
              child: ListTile(
                onTap: () => callback('contact handle goes here', '$num'),
                title: Text('contact handle goes here#$num'),
                subtitle: Text('last message'),
              ),
            );
          }),
    );
  }
}
