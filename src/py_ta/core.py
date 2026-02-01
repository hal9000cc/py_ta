"""Core data structures for py-ta."""


class DataSeries:
    """Base class for quotes and indicator results.
    
    Acts as a dictionary with attribute-style access.
    
    Example:
        >>> data = DataSeries({'value': [1, 2, 3], 'time': [...]})
        >>> print(data.value)
        [1, 2, 3]
    """
    
    def __init__(self, data_dict):
        """Initialize DataSeries with a dictionary of data.
        
        Args:
            data_dict: Dictionary containing numpy arrays or other data
        """
        self._data = data_dict
    
    def __getattr__(self, name):
        """Get attribute from internal data dictionary.
        
        Args:
            name: Attribute name
            
        Returns:
            Value from internal dictionary
            
        Raises:
            AttributeError: If attribute not found
        """
        if name.startswith('_'):
            # Avoid infinite recursion for internal attributes
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __repr__(self):
        """String representation of DataSeries."""
        keys = ', '.join(self._data.keys())
        return f"{type(self).__name__}({keys})"

