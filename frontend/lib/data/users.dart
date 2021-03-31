import 'package:rabbit_messenger_frontend/data/channels.dart';
import 'package:sqfentity_gen/sqfentity_gen.dart';

const usersTable = SqfEntityTable(
    tableName: "users",
    primaryKeyName: "user_id",
    primaryKeyType: PrimaryKeyType.text,
    useSoftDeleting: false,
    fields: [
      SqfEntityField("name", DbType.text),
      SqfEntityField("hash", DbType.text),
      SqfEntityFieldRelationship(
        parentTable: channelsTable,
        deleteRule: DeleteRule.NO_ACTION,
        relationType: RelationType.ONE_TO_MANY,
      ),
      // channel membership
      SqfEntityFieldRelationship(
        parentTable: channelsTable,
        deleteRule: DeleteRule.SET_NULL,
        relationType: RelationType.MANY_TO_MANY,
      ),
      // channel ownership. MANY TO MANY in case multiple users have admin rights
    ]);
