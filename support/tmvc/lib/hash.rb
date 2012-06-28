class Hash
  def filter(*keys)
    keys.flatten.inject({}) do |new_hash, key|
      new_hash[key] = self[key] if self[key]
      new_hash
    end
  end
  
  def stringify_keys!
    keys.each do |k|
      if k.is_a?(Symbol)
        value = delete(k)
        self[k.to_s] = value
      end
    end
  end
  
  # alias reject_without_params reject
  # def reject(*keys, &block)
  #   return reject_without_params(&block) if keys.empty?
  #   reject_without_params { |key,value| keys.include?(key)}
  # end
end