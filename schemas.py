from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    full_name = fields.Str(required=True)
    role = fields.Str(validate=validate.OneOf(["Student", "Staff", "Facilities", "Admin"]))

class RoomSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    building = fields.Str(required=True)
    capacity = fields.Int(required=True)
    equipment = fields.Str()
    room_type = fields.Str()
    status = fields.Str()

class BookingSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    room_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    status = fields.Str()

class MaintenanceIssueSchema(Schema):
    id = fields.Int(dump_only=True)
    room_id = fields.Int(required=True)
    description = fields.Str(required=True)
    issue_type = fields.Str()
    priority = fields.Str(validate=validate.OneOf(["Low", "Medium", "High", "Critical"]))
    status = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class FeedbackSchema(Schema):
    id = fields.Int(dump_only=True)
    room_id = fields.Int(required=True)
    rating = fields.Int(validate=validate.Range(min=1, max=5))
    comment = fields.Str()
