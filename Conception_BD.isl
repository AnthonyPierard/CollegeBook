system "CollegeBooking" "CB";
  date 140223
  graph
    zoom 100
    reduce 100
    grid 0 0
    font 0 ""
  end-graph
  meta-object "Project";
    object-type "1"
  end-meta-object

  meta-object "Schema";
    object-type "2"
    meta-property "productType";
      type "string" updatable predefined
      description SEM;
#VALUES=
COBOL
CODASYL
IMS
Relational
SQL
XML
C/C++
Java
#
      end-description
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
    meta-property "GHSPosX";
      type "int" system
    end-meta-property
    meta-property "GHSPosY";
      type "int" system
    end-meta-property
  end-meta-object

  meta-object "Text";
    object-type "31"
    meta-property "productType";
      type "string" updatable predefined
      description SEM;
#VALUES=
COBOL
CODASYL
IMS
Relational
SQL
XML
C/C++
Java
#
      end-description
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Product set";
    object-type "41"
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Entity type";
    object-type "11"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Rel-type";
    object-type "12"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Atomic attribute";
    object-type "7"
    meta-property "Default value";
      type "string" updatable
    end-meta-property
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "physLen";
      type "int" updatable
    end-meta-property
    meta-property "physType";
      type "string" updatable
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
    meta-property "Value constraint";
      type "string" updatable multivalued
    end-meta-property
  end-meta-object

  meta-object "Compound attribute";
    object-type "6"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Group";
    object-type "16"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "User-constraint";
      type "string" system
    end-meta-property
  end-meta-object

  meta-object "Role";
    object-type "14"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Collection";
    object-type "4"
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
      description SEM;
#VALUES=
Area
DBD
SQLSchema
SubSchema
TableSpace
#
      end-description
    end-meta-property
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
  end-meta-object

  meta-object "Processing unit";
    object-type "40"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Processing unit relation";
    object-type "45"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Association";
    object-type "47"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Use case association role";
    object-type "68"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Actor association role";
    object-type "66"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Actor";
    object-type "48"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "Actor generalization";
    object-type "62"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

  meta-object "State";
    object-type "61"
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
      description SEM;
#VALUES=
ET
RT
Att
Coll
#
      end-description
    end-meta-property
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
  end-meta-object

  meta-object "In-out";
    object-type "43"
    meta-property "MappingOID";
      type "int" updatable multivalued
    end-meta-property
    meta-property "Stereotype";
      type "string" updatable multivalued predefined
    end-meta-property
  end-meta-object

end-system
