import 'package:sqfentity_gen/sqfentity_gen.dart';
import 'users.dart';

const channelsTable = SqfEntityTable(
    tableName: "channels",
    primaryKeyName: "channel_id",
    primaryKeyType: PrimaryKeyType.integer_unique,
    useSoftDeleting: false,
    fields: [
      SqfEntityField("id", DbType.integer),
      SqfEntityField("type", DbType.text),
    ]);
