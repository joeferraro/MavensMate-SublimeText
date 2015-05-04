trigger {{ api_name }} on {{ object_name }} (before insert, before update, before delete, after insert, after update, after delete, after undelete) {

	for ({{ object_name }} so : Trigger.new) {
		//friends remind friends to bulkify
	}

}