# encoding: utf-8
require 'date.rb'
require 'time.rb'

module FriendlyTime
  def to_friendly(time=true)
    time=false if Date==self.class
    
    ret_val = if time
      strftime "%b %d, %Y %I:%M %p" + (time=="zone"? " %Z" : "")
    else
      strftime "%b %d, %Y"
    end
    
    ret_val.gsub(" 0", " ")
  end
end

class Time; include FriendlyTime; end
class Date; include FriendlyTime; end
class DateTime; include FriendlyTime; end

module DateHelpers
  def distance_of_time_in_words(from_time, to_time = 0, include_seconds = false)
    from_time = from_time.to_time if from_time.respond_to?(:to_time)
    to_time = to_time.to_time if to_time.respond_to?(:to_time)
    distance_in_minutes = (((to_time - from_time).abs)/60).round
    distance_in_seconds = ((to_time - from_time).abs).round
  
    case distance_in_minutes
      when 0..1
        return (distance_in_minutes == 0) ? 'less than a minute' : '1 minute' unless include_seconds
        case distance_in_seconds
          when 0..4   then '< 5 seconds'
          when 5..9   then '< 10 seconds'
          when 10..19 then '< 20 seconds'
          when 20..39 then '½ minute'
          when 40..59 then '< a minute'
          else             '1 minute'
        end
    
      when 2..44           then "#{distance_in_minutes} minutes"
      when 45..89          then '~1 hour'
      when 90..1439        then "~#{(distance_in_minutes.to_f / 60.0).round} hours"
      when 1440..2879      then '1 day'
      when 2880..43199     then "#{(distance_in_minutes / 1440).round} days"
      when 43200..86399    then '~1 month'
      when 86400..525599   then "#{(distance_in_minutes / 43200).round} months"
      when 525600..1051199 then '~1 year'
      else                      "> #{(distance_in_minutes / 525600).round} years"
    end
  end

  def relative_date(date)
    return date if date.is_a?(String)
    distance_of_time_in_words(Time.now, date)
  end
end